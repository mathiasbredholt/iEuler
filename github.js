var page = require('webpage').create();
page.open('/Users/mathiasbredholt/Documents/iEuler/mathnotesgui/webkit/test.html', function() {
  page.render('github.png');
  phantom.exit();
});
