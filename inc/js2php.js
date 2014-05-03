global.fs = require('fs');


var variables = [];

var replacements = [
  {
    pattern: /var ([a-z0-9_]+)/gi,
    replacement: function (z, a) {
      variables.push(a);
      return '$' + a;
    },
  },


  {
    pattern: /=\s*function\s*\((?:\$?([^,\)]+),?\s*)+\)/gi,
    replacement: function (z, a) {
      variables.push(a);
      return z;
    },
  },

  {
    pattern: /([a-z0-9_]+)\s*=\s*function\(/gi,
    replacement: 'function $1($$',
  },
  {
    pattern: /req\.body/gi,
    replacement: '$$params',
  },
  {
    pattern: /req\.params/gi,
    replacement: '$$params',
  },
  {
    pattern: /res\.Page\.sysnotes\./gi,
    replacement: 'Sysnote::',
  },
  {
    pattern: /return res\.Page\.footer\(\);/gi,
    replacement: 'exit;',
  },
  {
    pattern: /re[sq]\./gi,
    replacement: '$$',
  },
  {
    pattern: /api\.([a-z]+)\./gi,
    replacement: function (z, a) {
      return a.slice(0, 1).toUpperCase() + a.slice(1) + '::';
    },
  },
  {
    pattern: /([a-z0-9]+:*[a-z0-9]+)\((.*),\s*function\(err, ([a-z]+)\)\{/gi,
    replacement: '$$$3 = $1($$$2)',
  },
  {
    pattern: /(\$[a-z]+)\.([a-z]+(?!\())\b/gi,
    replacement: '$1[\'$2\']',
  },

  {
    pattern: /\{\}/gi,
    replacement: '[]',
  },


  {
    pattern: /\{([\s\n\r]*[a-z0-9_]+\s*:(?!:)\s*[^,\}]+,?)*[\s\n\r]*\}/gi,
    replacement: function (z, a) {
      return '[' + (z || '').slice(1, -1).replace(/[\s\n\r]*([a-z0-9_]+)\s*:\s*([^,\}]+)[\s\n\r]*[,}]?/gi, '\'$1\' => $2,\n') + ']';
    },
  },


  {
    pattern: /\]\.([a-z0-9_]+)/gi,
    replacement: '][\'$1\']',
  },
  {
    pattern: /(['"])\s*\+/gi,
    replacement: '$1 . ',
  },
  {
    pattern: /\+\s*(['"])/gi,
    replacement: ' . $1',
  },
  {
    pattern: /_\.each\(([^,]+),\s*function\(([^,]+),\s*(.+)\)\s*\{/gi,
    //replacement : 'foreach($1 as $3 => $2){',
    replacement: function (z, a, b, c) {
      return 'foreach(' + (a.slice(0, 1) == '$' ? '' : '$') + a + ' as ' + (c.slice(0, 1) == '$' ? '' : '$') + c + ' => ' + (b.slice(0, 1) == '$' ? '' : '$') + b + '){'
    },
  },
  {
    pattern: /_\.each\(([^,]+),\s*function\((.+)\)\s*\{/gi,
    //replacement : 'foreach($1 as $2){',
    replacement: function (z, a, b) {
      return 'foreach(' + (a.slice(0, 1) == '$' ? '' : '$') + a + ' as ' + (b.slice(0, 1) == '$' ? '' : '$') + b + '){'
    },
  },

  {
    pattern: /\.push\((.*)\);/gi,
    replacement: '[] = $1;',
  },

  // run this one multiple times
  {
    pattern: /([a-z0-9_]+)\.([a-z0-9_]+)([,;\s\)\[])/gi,
    replacement: '$1[\'$2\']$3',
  },
  {
    pattern: /([a-z0-9_]+)\.([a-z0-9_]+)([,;\s\)\[])/gi,
    replacement: '$1[\'$2\']$3',
  },
  {
    pattern: /([a-z0-9_]+)\.([a-z0-9_]+)([,;\s\)\[])/gi,
    replacement: '$1[\'$2\']$3',
  },

  {
    pattern: /\$Page\./gi,
    replacement: '$Page->',
  },
  {
    pattern: /\$Page\['title'\]/gi,
    replacement: '$Page->title',
  },
  {
    pattern: /\$Page\['json'\]/gi,
    replacement: '$Page->json',
  },




  {
    pattern: /Math\./gi,
    replacement: '',
  },
  {
    pattern: /Users::usernotes\./gi,
    replacement: 'UserUsernotes::',
  },




  {
    pattern: /([\$\s\(])([a-z0-9_]+)\['length'\]/gi,
    replacement: '$1count($2)',
  },{
    pattern: /Math\./gi,
    replacement: '',
  },





  {
    pattern: /_\.unique/gi,
    replacement: 'array_unique',
  },
  {
    pattern: /_\.size/gi,
    replacement: 'count',
  },
  ,
  {
    pattern: /_\.m(in|ax)/gi,
    replacement: 'm$1',
  },

  {
    pattern: /\{\s*-?%>/gi,
    replacement: ': ?>',
  },
  {
    pattern: /-?%>/gi,
    replacement: '?>',
  },
  {
    pattern: /<%-/gi,
    replacement: '<?php echo',
  },
  {
    pattern: /<%=/gi,
    replacement: '<?php echo ent()',
  },
  {
    pattern: /<%/gi,
    replacement: '<?php',
  },
  {
    pattern: /locals\['([a-z0-9_]+)'\]/gi,
    replacement: '$$$1',
  },
  {
    pattern: /locals\.\$?/gi,
    replacement: '$$',
  },{
    pattern: /<\?php\s*\}\s*else/gi,
    replacement: '<?php else',
  }





//  {
//    pattern: /a/gi,
//    replacement: 'a',
//  },
//  {
//    pattern: /_\.union\(([^,\(]+(?:\([^\)]\))*)+,/gi,
//    replacement: 'test',
//  },


  /*
   {
   pattern: /a/gi,
   replacement : '',
   },*/
];


/**
 * escapes characters that are used in regular expressions
 */
regQuote = function (str, delimiter) {
  return (str + '').replace(new RegExp('[.\\\\+*?\\[\\^\\]$(){}=!<>|:\\' + (delimiter || '') + '-]', 'g'), '\\$&');
};

var folder = process.argv[2] || '';
//console.log(folder + '../temp/js2phpIn.txt');
//return;

var content = fs.readFileSync(folder + '../temp/js2phpIn.txt');


content = (content || '').toString();

for (var k in replacements) {
  content = content.replace(replacements[k].pattern, replacements[k].replacement);
}

for (var k in variables) {
  var reg = new RegExp('([^$\'"\/])\\b(' + regQuote(variables[k]) + ')\\b', 'g');
  content = content.replace(reg, '$1$$$2')
}


console.log(content);
//console.log(variables);

//emmiter1.on('this_event',callback);