$(function () {

    function CalculateReadingAge(textSpan,editorParent) {
        // Constants for our reading level calculation
        // These are part of the Automated Readability Index calculation
        // https://en.wikipedia.org/wiki/Automated_readability_index
        var CHARACTER_WEIGHT = 4.71;
        var SENTENCE_WEIGHT = 0.5;
        var BASE = 21.43;

        // Turn the html into plain text
        var text = textSpan.text();

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
            editorParent.find('p.readinglevel').html("<strong>Reading age:</strong> " + readingAge);
            return readingAge;
        }
        else {
            editorParent.find('p.readinglevel').html("<strong>Reading age:</strong> Not enough content to calculate age score.");
            return null;
        }
    }

    function SetUpEditors() {
        // REGULAR RICH TEXT AREAS -----------------------------------------------
        // Get all of the regular rich text areas (non-streamfield)
        var editors = $('span').find('[data-text="true"]')
        if(editors) {
            editors.each(function() {
    
                var editor = $(this);
                var editorParent = editor.parent().parent().parent().parent().parent().parent().parent().parent();
                var helpTextContainer = editorParent.find('.help');
                if (helpTextContainer.html()) {
                    helpTextContainer.addClass('readinglevel');
                }
                else {
                    // Didn't find an existing help box so create one with our custom class
                    editorParent.append("<p class='help readinglevel'><strong>Reading age:</strong>" + 
                                            " Not enough content to calculate age score.</p>");
                }
                // console.log(editor.children());
                var readingAge = CalculateReadingAge(editor, editorParent);
                setInterval(()=>CheckEditors(), 1000);
            });
        }
    }

    function CheckEditors() {
        // REGULAR RICH TEXT AREAS -----------------------------------------------
        // Get all of the regular rich text areas (non-streamfield)
        var editors = $('span').find('[data-text="true"]')

        editors.each(function() {

            var editor = $(this);
            var editorParent = editor.parent().parent().parent().parent().parent().parent().parent().parent();
            // console.log(editor.children());
            var readingAge = CalculateReadingAge(editor, editorParent);
        });
    }

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
    WatchStreamFields()

});
