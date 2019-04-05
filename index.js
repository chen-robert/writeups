const express = require("express");
const mds = require("markdown-serve");
const path = require("path");

const serveIndex = require("serve-index");

const app = express();
app.set("views", __dirname + "/views");
app.set("view engine", "ejs");

app.use((req, res, next) => {
  if(req.path.endsWith(".md")) {
    return res.redirect(req.path.substring(0, req.path.length - 3));
  }
  next();
});
app.use(serveIndex("data", {icons: true}));
app.use(express.static(__dirname + "/data"));
app.use("/docs", mds.middleware({
  rootDirectory: path.resolve(__dirname, "data/docs"),
  view: "docs"
}));
app.use("/slides", mds.middleware({
  rootDirectory: path.resolve(__dirname, "data/slides"),
  view: "slides",
  preParse: markdownFile => {
    return {
      title: markdownFile.meta.title || markdownFile.meta,
      rawContent: markdownFile.rawContent,
      content: markdownFile.parseContent()
    }
  }
}));

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Listening on port ${PORT}`));
