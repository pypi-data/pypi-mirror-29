/*
 * Copyright 2015-2018 Guardtime, Inc.
 *
 * This file is part of the Guardtime client SDK.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *     http://www.apache.org/licenses/LICENSE-2.0
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES, CONDITIONS, OR OTHER LICENSES OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 * "Guardtime" and "KSI" are trademarks or registered trademarks of
 * Guardtime, Inc., and no license to trademarks is granted; Guardtime
 * reserves and retains all trademark rights.
 */

#include <Python.h>
#include <ksi/ksi.h>

#define Py_LIMITED_API

// backward compatibility for format string: blob as string or bytes
#if PY_MAJOR_VERSION >= 3
    #define _SoB_ "y#"
    #define string_from_object(py_obj) PyBytes_AsString(PyUnicode_AsUTF8String(py_obj))
#else
    #define _SoB_ "s#"
    #define string_from_object(py_obj) PyString_AsString(py_obj)
#endif

// Some verification policies.
#define POLICY_EXTEND   (1<<6)
#define POLICY_KEY_BASED 1
#define POLICY_CALENDAR_BASED 2
#define POLICY_PUBLICATIONS_FILE_BASED 3
#define POLICY_PUBLICATIONS_FILE_BASED_EXT (POLICY_PUBLICATIONS_FILE_BASED | POLICY_EXTEND)
#define POLICY_GENERAL 4
#define POLICY_GENERAL_EXT (POLICY_GENERAL | POLICY_EXTEND)

PyObject *import_exception(char* name) {
    PyObject *module, *result = NULL;

    module = PyImport_ImportModule("ksi");
    if (module) {
        result = PyDict_GetItemString(PyModule_GetDict(module), name);
    }
    if (!result) {
        result = PyExc_RuntimeError;
        // note that this error will be overwritten
        PyErr_SetString(PyExc_RuntimeError, "Can not find exception in module");
    }
    return result;
}

PyObject *get_exception_obj(int code) {
    switch (code) {
        case KSI_OUT_OF_MEMORY:
            return PyExc_MemoryError;

		case KSI_AGGREGATOR_NOT_CONFIGURED:
		case KSI_EXTENDER_NOT_CONFIGURED:
		case KSI_PUBLICATIONS_FILE_NOT_CONFIGURED:
		case KSI_PUBFILE_VERIFICATION_NOT_CONFIGURED:
		case KSI_INVALID_VERIFICATION_INPUT:
            return import_exception("ConfigurationError");

		case KSI_INVALID_ARGUMENT:
		case KSI_INVALID_FORMAT:
		case KSI_UNTRUSTED_HASH_ALGORITHM:
		case KSI_UNAVAILABLE_HASH_ALGORITHM:
            return import_exception("FormatError");

		case KSI_INVALID_SIGNATURE:
		case KSI_INVALID_PKI_SIGNATURE:
		case KSI_PKI_CERTIFICATE_NOT_TRUSTED:
		case KSI_INVALID_STATE:
            return import_exception("InvalidSignatureError");

		case KSI_IO_ERROR:
            return PyExc_IOError;

        case KSI_NETWORK_ERROR:
        case KSI_NETWORK_CONNECTION_TIMEOUT:
        case KSI_NETWORK_SEND_TIMEOUT:
        case KSI_NETWORK_RECIEVE_TIMEOUT:
        case KSI_HTTP_ERROR:
            return import_exception("NetworkError");

		case KSI_EXTEND_WRONG_CAL_CHAIN:

		case KSI_EXTEND_NO_SUITABLE_PUBLICATION:
		case KSI_VERIFICATION_FAILURE:
		case KSI_INVALID_PUBLICATION:
		case KSI_PUBLICATIONS_FILE_NOT_SIGNED_WITH_PKI:
            return import_exception("PublicationError");

		case KSI_CRYPTO_FAILURE:
            return import_exception("CryptoError");

		case KSI_SERVICE_AUTHENTICATION_FAILURE:
            return import_exception("ServiceAuthError");

		case KSI_REQUEST_PENDING:
		case KSI_HMAC_MISMATCH:
		case KSI_HMAC_ALGORITHM_MISMATCH:
		case KSI_UNSUPPORTED_PDU_VERSION:
		case KSI_SERVICE_INVALID_REQUEST:
		case KSI_SERVICE_INVALID_PAYLOAD:
		case KSI_SERVICE_INTERNAL_ERROR:
		case KSI_SERVICE_UPSTREAM_ERROR:
		case KSI_SERVICE_UPSTREAM_TIMEOUT:
		case KSI_SERVICE_AGGR_REQUEST_TOO_LARGE:
		case KSI_SERVICE_AGGR_REQUEST_OVER_QUOTA:
		case KSI_SERVICE_AGGR_INPUT_TOO_LONG:
		case KSI_SERVICE_AGGR_TOO_MANY_REQUESTS:
		case KSI_SERVICE_AGGR_PDU_V2_RESPONSE_TO_PDU_V1_REQUEST:
		case KSI_SERVICE_AGGR_PDU_V1_RESPONSE_TO_PDU_V2_REQUEST:

		case KSI_SERVICE_EXTENDER_PDU_V2_RESPONSE_TO_PDU_V1_REQUEST:
		case KSI_SERVICE_EXTENDER_PDU_V1_RESPONSE_TO_PDU_V2_REQUEST:
		case KSI_SERVICE_UNKNOWN_ERROR:
            return import_exception("ServiceError");

		case KSI_SERVICE_EXTENDER_INVALID_TIME_RANGE:
		case KSI_SERVICE_EXTENDER_DATABASE_MISSING:
		case KSI_SERVICE_EXTENDER_DATABASE_CORRUPT:
		case KSI_SERVICE_EXTENDER_REQUEST_TIME_TOO_OLD:
		case KSI_SERVICE_EXTENDER_REQUEST_TIME_TOO_NEW:
		case KSI_SERVICE_EXTENDER_REQUEST_TIME_IN_FUTURE:
            return import_exception("ServiceExtenderBlockchainError");

		case KSI_BUFFER_OVERFLOW:
		case KSI_TLV_PAYLOAD_TYPE_MISMATCH:
		case KSI_ASYNC_NOT_FINISHED:

		case KSI_ASYNC_CONNECTION_CLOSED:
		case KSI_ASYNC_REQUEST_CACHE_FULL:
		case KSI_UNKNOWN_ERROR:
        default:
            return import_exception("Error");
    }
}

static void format_exception(KSI_CTX *ctx, int res, int line) {
    char buf[512];
    PyObject *s;

    if (KSI_ERR_getBaseErrorMessage(ctx, buf, sizeof(buf), NULL, NULL) == KSI_OK) {
        s = PyBytes_FromFormat("L%04d: %s <%s>", line, KSI_getErrorString(res), buf);
    } else {
        s = PyBytes_FromFormat("L%04d: %s", line, KSI_getErrorString(res));
    }
    PyErr_SetObject(get_exception_obj(res), s);
    Py_DECREF(s);
}

#define EH(plah) { int _res = (plah);  \
            if (_res != KSI_OK) { \
                format_exception(ctx, _res, __LINE__); \
                goto cleanup; \
            }};

//  no KSI_CTX available:
#define EHX(plah) { int _res = (plah);  \
            if (_res != KSI_OK) { \
                 PyErr_SetString(PyExc_Exception, KSI_getErrorString(_res)) ; \
                 goto cleanup; \
             }};

static PyObject *
ksi_init(PyObject *self, PyObject *args) {
    const char *surl, *suser, *skey;
    const char *xurl, *xuser, *xkey;
    const char *purl;
    PyObject *cnstr_obj = NULL;
    PyObject *key_obj = NULL, *val_obj = NULL;
    Py_ssize_t pos = 0;
    KSI_CertConstraint *pcnstr = NULL;
    int i = 0;
    long len = 0;
    KSI_CTX *ctx = NULL;

    if (!PyArg_ParseTuple(args, "sssssssO:ksi_init", &surl, &suser, &skey,
                          &xurl, &xuser, &xkey, &purl, &cnstr_obj)) {
        goto cleanup;
    }

    len = (PyDict_Size(cnstr_obj)) + 1;
    pcnstr = calloc(len, sizeof(KSI_CertConstraint));
    if (pcnstr == NULL) {
        goto cleanup;
    }

    while (PyDict_Next(cnstr_obj, &pos, &key_obj, &val_obj)) {
        if (key_obj != NULL && val_obj != NULL) {
            char *tmp_oid = string_from_object(key_obj);

            /* Check if it is an alias string representation of the OID */
            if (strncmp(tmp_oid, "email", 5) == 0) {
                tmp_oid = KSI_CERT_EMAIL;
            } else if (strncmp(tmp_oid, "country", 7) == 0) {
                tmp_oid = KSI_CERT_COUNTRY;
            } else if (strncmp(tmp_oid, "org", 3) == 0) {
                tmp_oid = KSI_CERT_ORGANIZATION;
            } else if (strncmp(tmp_oid, "common_name", 11) == 0) {
                tmp_oid = KSI_CERT_COMMON_NAME;
            }

            pcnstr[i].oid = tmp_oid;
            pcnstr[i].val = string_from_object(val_obj);
        }
        i++;
    }
    pcnstr[i].oid = NULL;
    pcnstr[i].val = NULL;

    EH( KSI_CTX_new(&ctx) );
    EH( KSI_CTX_setAggregator(ctx, surl, suser, skey) );
    EH( KSI_CTX_setExtender(ctx, xurl, xuser, xkey) );
    EH( KSI_CTX_setPublicationUrl(ctx, purl) );
    EH( KSI_CTX_setDefaultPubFileCertConstraints(ctx, pcnstr) );
    free(pcnstr);
    return Py_BuildValue("K", (intptr_t) ctx);

cleanup:
    free(pcnstr);
    KSI_CTX_free(ctx);
    return NULL;
}

// Must be called after cleaning up all created signatures.
static PyObject *
ksi_cleanup(PyObject *self, PyObject *args) {
    long long ctx_long;

    if (!PyArg_ParseTuple(args, "K:ksi_cleanup", &ctx_long)) {
        return NULL;
    }
    KSI_CTX *ctx = (KSI_CTX *) (intptr_t) ctx_long;
    KSI_CTX_free(ctx);
    Py_RETURN_NONE;
}


static PyObject *
ksi_sign(PyObject *self, PyObject *args) {
    const char *hashalgname = NULL;
    int hashalgid = 0;
    const unsigned char *hash_bytes = NULL;
    int hash_len = 0;
    long long ctx_long;
    KSI_Signature *sig = NULL;
    KSI_DataHash *hash = NULL;
    PyObject *py_result = NULL;

    if (!PyArg_ParseTuple(args, "Ls"_SoB_":ksi_sign", &ctx_long, &hashalgname, &hash_bytes, &hash_len)) {
        goto cleanup;
    }
    KSI_CTX *ctx = (KSI_CTX *) (intptr_t) ctx_long;
    hashalgid = KSI_getHashAlgorithmByName(hashalgname);
    if (hashalgid == -1) {
        PyErr_SetString(PyExc_Exception, "Unknown hash algorithm");
        goto cleanup;
    }
    EH( KSI_DataHash_fromDigest(ctx, hashalgid, hash_bytes, hash_len, &hash) );
    EH( KSI_createSignature(ctx, hash, &sig) );
    py_result = Py_BuildValue("K", (intptr_t) sig);
cleanup:
    KSI_DataHash_free(hash);
    return py_result;
}

static PyObject *
ksi_cleanup_sig(PyObject *self, PyObject *args) {
    long long sig_long;

    if (!PyArg_ParseTuple(args, "K:ksi_cleanup_sig", &sig_long)) {
        goto cleanup;
    }
    KSI_Signature *sig = (KSI_Signature *) (intptr_t) sig_long;

    KSI_Signature_free(sig);
    Py_RETURN_NONE; // returns
cleanup:
    return NULL;
}

// TODO: consider integrating with other verification functions
static PyObject *
ksi_verify_sig(PyObject *self, PyObject *args) {
    long long ctx_long;
    long long sig_long;

    if (!PyArg_ParseTuple(args, "KK:ksi_verify_sig", &ctx_long, &sig_long)) {
        goto cleanup;
    }
    KSI_CTX *ctx = (KSI_CTX *) (intptr_t) ctx_long;
    KSI_Signature *sig = (KSI_Signature *) (intptr_t) sig_long;
    EH( KSI_verifySignature(ctx, sig) );
    Py_RETURN_NONE; // returns
cleanup:
    return NULL;
}

// TODO: consider removing later.
static PyObject *
ksi_verify_hash(PyObject *self, PyObject *args) {
    long long ctx_long;
    long long sig_long;
    const char *hashalgname = NULL;
    const unsigned char *hash_bytes = NULL;
    int hashalgid = 0;
    int hash_len = 0;
    KSI_DataHash *hash = NULL;
    int ret = KSI_OK;
    PyObject *py_result = NULL;

    if (!PyArg_ParseTuple(args, "KKs"_SoB_":ksi_verify_hash", &ctx_long, &sig_long, &hashalgname, &hash_bytes, &hash_len)) {
        goto cleanup;
    }
    KSI_CTX *ctx = (KSI_CTX *) (intptr_t) ctx_long;
    KSI_Signature *sig = (KSI_Signature *) (intptr_t) sig_long;
    hashalgid = KSI_getHashAlgorithmByName(hashalgname);
    if (hashalgid == -1) {
        PyErr_SetString(PyExc_Exception, "Unknown hash algorithm");
        goto cleanup;
    }
    EH( KSI_DataHash_fromDigest(ctx, hashalgid, hash_bytes, hash_len, &hash) );
    ret = KSI_verifyDataHash(ctx, sig, hash);
    switch(ret) {
        case KSI_OK:
            Py_INCREF(Py_True);
            py_result = Py_True;
            break;
        case KSI_VERIFICATION_FAILURE:
            Py_INCREF(Py_False);
            py_result = Py_False;
            break;
        default:
            EH( ret );
            break;
    }
cleanup:
    KSI_DataHash_free(hash);
    return py_result;
}

static PyObject *
ksi_verify_hash_with_policy(PyObject *self, PyObject *args) {
    long long ctx_long;
    long long sig_long;
    const char *hashalgname = NULL;
    const unsigned char *hash_bytes = NULL;
    int hashalgid = 0;
    int hash_len = 0;
    int policy_int;

    KSI_DataHash *hash = NULL;
    const KSI_Policy *policy;
    KSI_VerificationContext context;
    KSI_PolicyVerificationResult *result = NULL;
    PyObject *s;
    PyObject *py_result = NULL;


    if (!PyArg_ParseTuple(args, "KKs"_SoB_"i:ksi_verify_hash_with_policy",
                              &ctx_long, &sig_long, &hashalgname, &hash_bytes,
                              &hash_len, &policy_int)) {
        goto cleanup;
    }
    KSI_CTX *ctx = (KSI_CTX *) (intptr_t) ctx_long;

    switch(policy_int) {
        case POLICY_KEY_BASED:
            policy = KSI_VERIFICATION_POLICY_KEY_BASED;
            break;
        case POLICY_CALENDAR_BASED:
            policy = KSI_VERIFICATION_POLICY_CALENDAR_BASED;
            break;
        case POLICY_PUBLICATIONS_FILE_BASED:
        case POLICY_PUBLICATIONS_FILE_BASED_EXT:
            policy = KSI_VERIFICATION_POLICY_PUBLICATIONS_FILE_BASED;
            break;
        case POLICY_GENERAL:
        case POLICY_GENERAL_EXT:
            policy = KSI_VERIFICATION_POLICY_GENERAL;
            break;
        default:
            PyErr_SetString(PyExc_Exception, "Unsupported verification policy requested");
            goto cleanup;
    }

    hashalgid = KSI_getHashAlgorithmByName(hashalgname);
    if (hashalgid == -1) {
        PyErr_SetString(PyExc_Exception, "Unknown hash algorithm");
        goto cleanup;
    }
    EH( KSI_DataHash_fromDigest(ctx, hashalgid, hash_bytes, hash_len, &hash) );
    EH( KSI_VerificationContext_init(&context, ctx) );
    context.signature = (KSI_Signature *) (intptr_t) sig_long;
    context.documentHash = hash;
    context.extendingAllowed = (policy_int & POLICY_EXTEND) == POLICY_EXTEND;
    EH( KSI_SignatureVerifier_verify(policy, &context, &result) );

    switch(result->finalResult.resultCode) {
        case KSI_VER_RES_OK:     // ok, return true
            py_result = Py_BuildValue("(Oss)", Py_True, "OK", "OK");
            break;
        case KSI_VER_RES_FAIL:   // broken, return false.
            py_result = Py_BuildValue("(Oss)", Py_False,
                   KSI_VerificationErrorCode_toString(result->finalResult.errorCode),
                   KSI_Policy_getErrorString(result->finalResult.errorCode));
            break;
        case KSI_VER_RES_NA:     // no definitive answer.
        default:                 // Should not happen
            s = PyBytes_FromFormat("%s. Stopped at rule: %s",
                          KSI_Policy_getErrorString(result->finalResult.errorCode), result->finalResult.ruleName);
            PyErr_SetObject(PyExc_ValueError, s);
            Py_DECREF(s);
            goto cleanup;

    }

cleanup:
    KSI_VerificationContext_clean(&context);
    KSI_PolicyVerificationResult_free(result);
    KSI_DataHash_free(hash);
    return py_result;
}

static PyObject *
ksi_serialize(PyObject *self, PyObject *args) {
    long long sig_long;
    unsigned char *serialized = NULL;
    size_t serialized_len = 0;
    PyObject *py_result = NULL;

    if (!PyArg_ParseTuple(args, "K:ksi_serialize", &sig_long)) {
        goto cleanup;
    }
    KSI_Signature *sig = (KSI_Signature *) (intptr_t) sig_long;
    EHX( KSI_Signature_serialize(sig, &serialized, &serialized_len) );
    py_result = Py_BuildValue(_SoB_, serialized, (int)serialized_len);
cleanup:
    return py_result;
}

static PyObject *
ksi_parse(PyObject *self, PyObject *args) {
    long long ctx_long;
    unsigned char *serialized = NULL;
    int serialized_len = 0;
    PyObject *py_result = NULL;

    if (!PyArg_ParseTuple(args, "K"_SoB_":ksi_parse", &ctx_long, &serialized, &serialized_len)) {
        goto cleanup;
    }
    KSI_CTX *ctx = (KSI_CTX *) (intptr_t) ctx_long;
    KSI_Signature *sig = NULL;
    EH( KSI_Signature_parse(ctx, serialized, serialized_len, &sig) );
    py_result = Py_BuildValue("K", (intptr_t) sig);
cleanup:
    return py_result;
}

static PyObject *
ksi_get_hash_algorithm(PyObject *self, PyObject *args) {
    long long sig_long;
    KSI_HashAlgorithm alg_id;
    PyObject *py_result = NULL;

    if (!PyArg_ParseTuple(args, "K:ksi_get_hash_algorithm", &sig_long)) {
        goto cleanup;
    }
    KSI_Signature *sig = (KSI_Signature *) (intptr_t) sig_long;
    EHX( KSI_Signature_getHashAlgorithm(sig, &alg_id) );
    const char * alg_name = KSI_getHashAlgorithmName(alg_id);
    if (alg_name == NULL) {
        PyErr_SetString(PyExc_Exception, "Unknown hash algorithm");
        goto cleanup;
    }
    py_result = Py_BuildValue("s", alg_name);
cleanup:
    return py_result;
}

static PyObject *
ksi_get_data_hash(PyObject *self, PyObject *args) {
    long long sig_long;
    KSI_DataHash *dh = NULL;
    PyObject *py_result = NULL;
    KSI_HashAlgorithm alg_id; // TODO: backward compatibility
    const unsigned char *digest;
    size_t digest_len;

    if (!PyArg_ParseTuple(args, "K:ksi_get_data_hash", &sig_long)) {
        goto cleanup;
    }
    KSI_Signature *sig = (KSI_Signature *) (intptr_t) sig_long;
    EHX( KSI_Signature_getDocumentHash(sig, &dh) );
    EHX( KSI_DataHash_extract(dh, &alg_id, &digest, &digest_len) );

    py_result = Py_BuildValue("(s:"_SoB_")",
                  KSI_getHashAlgorithmName(alg_id),
                  digest, digest_len);

cleanup:
    return py_result;
}

static PyObject *
ksi_get_signing_time(PyObject *self, PyObject *args) {
    long long sig_long = 0;
    KSI_Integer *sigTime = NULL;
    PyObject *py_result = NULL;

    if (!PyArg_ParseTuple(args, "K:ksi_get_signing_time", &sig_long)) {
        goto cleanup;
    }
    KSI_Signature *sig = (KSI_Signature *) (intptr_t) sig_long;
    EHX( KSI_Signature_getSigningTime(sig, &sigTime) );
    py_result = PyLong_FromUnsignedLongLong(KSI_Integer_getUInt64(sigTime));
cleanup:
    // DO NOT FREE! KSI_Integer_free(sigTime);
    return py_result;
}

static PyObject *
ksi_get_signer_id(PyObject *self, PyObject *args) {
    long long sig_long;
    char id[512];
    KSI_HashChainLinkIdentityList *il = NULL;
    PyObject *py_result = NULL;

    if (!PyArg_ParseTuple(args, "K:ksi_get_signer_id", &sig_long)) {
        goto cleanup;
    }
    KSI_Signature *sig = (KSI_Signature *) (intptr_t) sig_long;
    EHX( KSI_Signature_getAggregationHashChainIdentity(sig, &il) );
    EHX( il == NULL ? KSI_INVALID_FORMAT : KSI_OK );
    size_t k;
    id[0] = '\0';
    for (k = 0; k < KSI_HashChainLinkIdentityList_length(il); k++) {
        size_t len = 0;
        KSI_HashChainLinkIdentity *identity = NULL;
        KSI_Utf8String *clientId = NULL;
        EHX( KSI_HashChainLinkIdentityList_elementAt(il, k, &identity));
        EHX( identity == NULL ? KSI_INVALID_FORMAT : KSI_OK );
        EHX( KSI_HashChainLinkIdentity_getClientId(identity, &clientId));
        EHX( identity == NULL ? KSI_INVALID_FORMAT : KSI_OK );
        len = strlen(id);
        snprintf(&id[len], sizeof(id) - len, "%s%s", (k > 0 ? " :: " : ""), KSI_Utf8String_cstr(clientId));
    }

    py_result = Py_BuildValue("s", id);
cleanup:
    return py_result;
}

static PyObject *
ksi_is_extended(PyObject *self, PyObject *args) {
    long long sig_long;
    PyObject *py_result = NULL;
    KSI_PublicationRecord *pubrec = NULL;

    if (!PyArg_ParseTuple(args, "K:ksi_is_extended", &sig_long)) {
        goto cleanup;
    }
    KSI_Signature *sig = (KSI_Signature *) (intptr_t) sig_long;
    EHX( KSI_Signature_getPublicationRecord(sig, &pubrec) );
    if (pubrec != NULL) {
        Py_INCREF(Py_True);
        py_result = Py_True;
    } else {
        Py_INCREF(Py_False);
        py_result = Py_False;
    }
cleanup:
    return py_result;
}

// extend signature token, return (true, extendedsig) if ok,
//     false if not yet possible, exc on error
static PyObject *
ksi_extend(PyObject *self, PyObject *args) {
    long long ctx_long;
    long long sig_long;
    KSI_Signature *ext = NULL;
    PyObject *py_result = NULL;

    if (!PyArg_ParseTuple(args, "KK:ksi_extend", &ctx_long, &sig_long)) {
        goto cleanup;
    }
    KSI_CTX *ctx = (KSI_CTX *) (intptr_t) ctx_long;
    KSI_Signature *sig = (KSI_Signature *) (intptr_t) sig_long;

    int ret = KSI_extendSignature(ctx, sig, &ext);
    switch(ret) {
        case KSI_OK:
            py_result = Py_BuildValue("OK", Py_True, (intptr_t) ext);
            break;
        case KSI_EXTEND_NO_SUITABLE_PUBLICATION:
            py_result = Py_BuildValue("OK", Py_False, (intptr_t) sig);
            break;
        default:
            EH( ret );
            break;
    }
cleanup:
    // sig must be freed by caller
    return py_result;
}

static PyObject *
ksi_get_publication_data(PyObject *self, PyObject *args) {
    long long sig_long;
    PyObject *py_result = PyDict_New();
    KSI_PublicationRecord *pubrec = NULL;
    KSI_PublicationData *pubdata = NULL;
    KSI_Integer *pubtime = NULL;
    char *pubstr = NULL;
    PyObject *py_pubtime = NULL;
    KSI_LIST(KSI_Utf8String) *pubrefs = NULL;
    PyObject* py_pubref_list = NULL;
    size_t i;

    if (!PyArg_ParseTuple(args, "K:ksi_get_publication_data", &sig_long)) {
        goto cleanup;
    }
    KSI_Signature *sig = (KSI_Signature *) (intptr_t) sig_long;
    EHX( KSI_Signature_getPublicationRecord(sig, &pubrec) );
    if (pubrec == NULL) {  // not extended / no pub. record
        py_result = Py_None;
        Py_INCREF(Py_None);
        goto cleanup;
    }
    EHX( KSI_PublicationRecord_getPublishedData(pubrec, &pubdata) );
    EHX( KSI_PublicationData_toBase32(pubdata, &pubstr) );
    EHX( KSI_PublicationData_getTime(pubdata, &pubtime) );

    py_pubtime = PyLong_FromUnsignedLongLong(KSI_Integer_getUInt64(pubtime));
    if (py_pubtime == NULL) {
        PyErr_SetString(PyExc_Exception, "PyLong_FromUnsignedLongLong() failed");
        goto cleanup;
    }
    EHX( KSI_PublicationRecord_getPublicationRefList(pubrec, &pubrefs) );
    if (pubrefs != NULL) {
        py_pubref_list = PyList_New(KSI_Utf8StringList_length(pubrefs));
        for (i = 0; i < KSI_Utf8StringList_length(pubrefs); i++) {
            KSI_Utf8String *ref = NULL;
            EHX( KSI_Utf8StringList_elementAt(pubrefs, i, &ref) );
            PyList_SET_ITEM(py_pubref_list, i, PyUnicode_FromString(KSI_Utf8String_cstr(ref)));
        }
    }

    py_result = Py_BuildValue("{s:s,s:O,s:O}",
                  "publication", pubstr,
                  "publishing_time_t", py_pubtime,
                  "refs", py_pubref_list
                  );
cleanup:
    KSI_free(pubstr);
    return py_result;
}


static PyMethodDef _KSIMethods[] = {
     {"ksi_init", ksi_init, METH_VARARGS, "Initialize KSI context."},
     {"ksi_cleanup", ksi_cleanup, METH_VARARGS, "Clean up passed KSI context."},
     {"ksi_sign", ksi_sign, METH_VARARGS, "Sign a hash."},
     {"ksi_serialize", ksi_serialize, METH_VARARGS, "Serialize a signature token."},
     {"ksi_parse", ksi_parse, METH_VARARGS, "Parse a data blob containing signature."},
     {"ksi_cleanup_sig", ksi_cleanup_sig, METH_VARARGS, "Clean up passed KSI_Signature."},
     {"ksi_verify_sig", ksi_verify_sig, METH_VARARGS, "Verify signature. Exception on any problems"},
     {"ksi_verify_hash", ksi_verify_hash, METH_VARARGS, "Check signature validity. Exception if unable."},
     {"ksi_verify_hash_with_policy", ksi_verify_hash_with_policy, METH_VARARGS, "Check signature validity. Exception if unable."},
     {"ksi_get_hash_algorithm", ksi_get_hash_algorithm, METH_VARARGS, "Get hash algorithm name."},
     {"ksi_get_data_hash", ksi_get_data_hash, METH_VARARGS, "Extract signed data hash from signature."},
     {"ksi_get_signing_time", ksi_get_signing_time, METH_VARARGS, "Get signing time."},
     {"ksi_get_signer_id", ksi_get_signer_id, METH_VARARGS, "Get signer's identity."},
     {"ksi_is_extended", ksi_is_extended, METH_VARARGS, "Check if signature token is extended."},
     {"ksi_extend", ksi_extend, METH_VARARGS, "Create a extended signature if possible. Input can be freed if OK."},
     {"ksi_get_publication_data", ksi_get_publication_data, METH_VARARGS, "Return publication properties from extended signature."},
     {NULL, NULL, 0, NULL}
};

PyObject *add_structs(PyObject *m) {
    // todo: namespace
    PyModule_AddIntMacro(m, POLICY_KEY_BASED);
    PyModule_AddIntMacro(m, POLICY_CALENDAR_BASED);
    PyModule_AddIntMacro(m, POLICY_PUBLICATIONS_FILE_BASED);
    PyModule_AddIntMacro(m, POLICY_PUBLICATIONS_FILE_BASED_EXT);
    PyModule_AddIntMacro(m, POLICY_GENERAL);
    PyModule_AddIntMacro(m, POLICY_GENERAL_EXT);

    return m;
}

#if PY_MAJOR_VERSION >= 3
    static struct PyModuleDef moduledef = {
            PyModuleDef_HEAD_INIT,
            "_ksi",
            NULL,
            0,
            _KSIMethods,
            NULL, NULL, NULL, NULL
    };

    PyObject *
    PyInit__ksi(void)
    {
        return add_structs(PyModule_Create(&moduledef));
    }

#else  // python 2.x

    PyMODINIT_FUNC init_ksi(void)
    {
        (void) add_structs(Py_InitModule("_ksi", _KSIMethods));
    }

#endif
