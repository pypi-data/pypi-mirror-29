$(function () {
    
        function CalculateReadingAge(textSpans, editor) {
            // Constants for our reading level calculation
            // These are part of the Automated Readability Index calculation
            // https://en.wikipedia.org/wiki/Automated_readability_index
            var CHARACTER_WEIGHT = 4.71;
            var SENTENCE_WEIGHT = 0.5;
            var BASE = 21.43;
    
            // Turn the html into plain text
            var text = textSpans;
    
            // Create the variables to hold the character, word and sentence counts
            var charCount = 0;
            var wordCount = 0;
            var sentenceCount = 0;
            
            // Calculate the character count
            charCount = text.length; 
    
            // Calculate the word count
            wordCount = text.split(" ").length;
    
            // Calculate the sentence count
            sentenceCount = (text.replace(/\w[.?!](\s|$)/g, "$1|").split("|").length) - 1;
    
            // If we have an empty first value in the array we know our text box is actually empty
            // so we need to minus 1 from our word count
            if(text.split(" ")[0] == "") {
                wordCount -= 1;
            }
    
            var readabilityScore = (CHARACTER_WEIGHT * (charCount / wordCount)) 
                + (SENTENCE_WEIGHT * (wordCount / sentenceCount)) - BASE;
    
            var readingAge = (readabilityScore + 4.).toFixed(1);
            // Modify the help area to include the new information
            if (isFinite(readingAge)) {
                if (readingAge > 18) { readingAge = "18+" }
                editor.find('.readinglevel').html("<strong>Reading age:</strong> " + readingAge);
                return readingAge;
            }
            else {
                editor.find('.readinglevel').html("<strong>Reading age:</strong> Not enough content to calculate age score.");
                return null;
            }
        }
    
        // Set up editors by adding help box and setting up interval checks.
        function SetUpEditors() {
            var editors = $('.Draftail-Editor');
            if(editors) {
                editors.each(function() {
                    var editor = $(this);
    
                    var textSpans = editor.find('[data-text="true"]')
                    var count = 0;
                    var text = "";
                    textSpans.each(function(){
                        var textSpan = $(this);
                        text += (textSpan.text() + "\n");
                        count ++;
                        if(count == textSpans.length){
                            var helpTextContainer = editor.find('.help');
                            if (helpTextContainer.html()) {
                                helpTextContainer.addClass('readinglevel');
                            }
                            else {
                                // Didn't find an existing help box so create one with our custom class
                                editor.append("<p class='help readinglevel'><strong>Reading age:</strong>" + 
                                                        " Not enough content to calculate age score.</p>");
                            }
                            var readingAge = CalculateReadingAge(text, editor);
                        }
                    });
                });
            }
        }
    
        // Check editors and text content. Update the reading ages appropriately.
        function CheckEditors() {
            var editors = $('.Draftail-Editor');
            
            editors.each(function() {
                var editor = $(this);
    
                var textSpans = editor.find('[data-text="true"]')
                var count = 0;
                var text = "";
                textSpans.each(function(){
                    var textSpan = $(this);
                    text += (textSpan.text() + "\n");
                    count ++;
                    if(count == textSpans.length){
                        var readingAge = CalculateReadingAge(text, editor);
                    }
                });
            });
        }
    
        // Watch the dom for structural changes using mutationobserver
        function WatchStreamFields() {
            var streamFields = document.querySelector('.stream-field');
            // We only want to observe if we have stream fields on the page
            if (streamFields) {
                var target = document.querySelector('.sequence');
    
                // create an observer instance
                var observer = new MutationObserver(function (mutations) {
                    mutations.forEach(function (mutation) {
                        SetUpEditors();
                    });
                });
    
                // configuration of the observer:
                var config = {
                    attributes: true,
                    childList: true,
                    characterData: true
                };
    
                // pass in the target node, as well as the observer options
                observer.observe(target, config);
            }
        }
    
        // Call the functions once on initial run
        SetUpEditors();
        WatchStreamFields();
        setInterval(()=>CheckEditors(), 1000);
    
    });
    