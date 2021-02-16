$(document).ready(function() {
  var button = $('#button');
  console.log('button', button)
  button.click(function() {
  makePost() //makePost() be called every time the button element is clicked. makePost() simply uses
             //the generated SDK to make a call to the POST endpoint we made earlier.
})
function makePost() {
    const text = $('#textbox').val();
    console.log('text', text);
    // newEntryPost takes (params, body, additionalParams)
    sdk.chatbotPost({}, {
    entry: 'here'
    }, {})
    .then(response => console.log('response', response))
  }
})
