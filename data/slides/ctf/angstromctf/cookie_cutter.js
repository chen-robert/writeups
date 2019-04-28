const jwt = require("jsonwebtoken");

let a = jwt.sign({secretid: "asdf", perms: "admin"}, "1", {algorithm: "none"});
let b = [1,2,3];
console.log(b["name"])
jwt.verify(a);

console.log(a);

