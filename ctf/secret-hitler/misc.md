# Misc Vulns 

Two low-moderate vulnerabilites. Note that a lot of the vulnerabilites are due to the use of [JSON parsing](https://github.com/cozuya/secret-hitler/blob/master/app.js#L64), which allows attackers to submit arbitrary objects to the endpoints.

## Obfuscated IP Leakage

The check in the `/profile` [endpoint](https://github.com/cozuya/secret-hitler/blob/master/routes/index.js#L204) is unnecessarily complex, and forgets an edge case.

```javascript
if (req && req.user && requestingUser && requestingUser !== 'undefined' && req.user.username && requestingUser !== req.user.username) {
  // Error 
}
```

Note that if the user is not signed in, then `req.user` becomes undefined. Thus, the branch becomes false and I am able to set `requestingUser` to whatever they want.

As a proof of concept, visit <https://secrethitler.io/profile?username=coz&requestingUser=coz> and note the inclusion of the `lastConnectedIP` attribute.

While the information leaked is somewhat useless - an obfuscated IP address, not the real IP - this would be useful to fix in case more information is included in the `/profile` endpoint later. 

## Email Leakage

Attackers could use the `/account/reset-password` [endpoint](https://github.com/cozuya/secret-hitler/blob/master/routes/accounts.js#L362) to leak emails from the database.

**This vulnerability can be mitigated by disabling JSON parsing.**

The `findOne` function with controlled inputs,

```javascript
Account.findOne({
  'verification.email': req.body.email
})
```

combined with predictable responses,

```javascript
.then(account => {
  if (!account) {
    // 401 response
    res.status(401).json(...);
  } else {
    // No response
    setVerify(...);
  }
```

means that the endpoint can act as a canary, lending itself to a standard blind injection.

As a proof of concept, consider the query

```javascript
req.body.email = {
  $gte: "a",
  $lte: "b"
}
```

This would error only if there was a verification email already between "a" and "b". In other words, the attacker will know if there is an email starting with the letter "a". By iteratively tightening the search constraints, for example with

```javascript
req.body.email = {
  $gte: "aa",
  $lte: "ab"
}
```

attackers can exfiltrate any number of email addresses from the database.


