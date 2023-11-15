var darkReaderScript = document.createElement('script');
darkReaderScript.src = 'https://cdn.jsdelivr.net/npm/darkreader@4.9.67/darkreader.min.js'


darkReaderScript.onload = function() {
    DarkReader.setFetchMethod(window.fetch);
    DarkReader.auto();
};


var head = document.head || document.getElementsByTagName('head')[0];
head.appendChild(darkReaderScript);