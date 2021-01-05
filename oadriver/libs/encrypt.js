const CryptoJS = require("crypto-js");

function encrypt(password) {
    var key = CryptoJS.MD5(Math.random() + '').toString();
    t = CryptoJS.AES.encrypt(password, key, {mode: CryptoJS.mode.CBC, padding: CryptoJS.pad.ZeroPadding});
    password_encode = t.ciphertext.toString(CryptoJS.enc.Base64);
    iv = t.iv.toString(CryptoJS.enc.Base64)
    key = t.key.toString(CryptoJS.enc.Base64)
    return {
        iv: iv,
        key: key,
        pass: password_encode
    };
}