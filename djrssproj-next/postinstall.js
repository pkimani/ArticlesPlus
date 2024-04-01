const fs = require("fs");
const path = require("path");

const pathArray = [
  "./node_modules/tr46/index.js",
  "./node_modules/nodemailer/lib/mime-node/index.js",
  "./node_modules/nodemailer/lib/dkim/sign.js",
];

try {
  for (const [i, value] of pathArray.entries()) {
    // Read the content of the file
    var tr46Path = path.resolve(value);
    var content = fs.readFileSync(tr46Path, "utf8");
    replace(content);
  }

  console.log("postinstall.js: Successfully patched tr46/index.js");
} catch (error) {
  console.error("postinstall.js: Error patching tr46/index.js", error);
}

function replace(content) {
  // Replace the problematic line
  content = content.replace(
    "const punycode = require('punycode');",
    "const punycode = require('punycode/');"
  );
  writeTheFile(content, tr46Path);
}

function writeTheFile(content, tr46Path) {
  // Write the modified content back to the file
  fs.writeFileSync(tr46Path, content, "utf8");
}
