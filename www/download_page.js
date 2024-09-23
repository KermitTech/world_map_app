

// alert("If you're seeing this, the javascript file was included successfully.");

// Shiny.addCustomMessageHandler('open_tab', function(url) {
//     console.log("Custom message handler called with URL: " + url);
//     if (url) {
//         window.open(url, '_blank');
//     } else {
//         console.log("No valid URL provided.");
//     }
// });

Shiny.addCustomMessageHandler('test_message', function(url) {
    if (url){
        window.open(url, '_blank');
    }
});