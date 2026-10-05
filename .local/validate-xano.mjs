import {xanoscriptParser} from 'file:///C:/Users/victo/.vscode/extensions/xano.xanoscript-language-server-0.3.3/language-server/parser/parser.js';
import fs from 'node:fs';
import path from 'node:path';
let errors=0, count=0;
function walk(dir) {
  for (const entry of fs.readdirSync(dir,{withFileTypes:true})) {
    const file=path.join(dir,entry.name);
    if(entry.isDirectory()) walk(file);
    else if(file.endsWith('.xs')) {
      count++;
      const result=xanoscriptParser(fs.readFileSync(file,'utf8'));
      if(result.errors.length) {
        errors++;
        console.log(file, JSON.stringify(result.errors.map(e => ({line:e.token?.startLine, message:e.message}))));
      }
    }
  }
}
walk('xano');
console.log({count,errors});
process.exitCode=errors?1:0;

