var state = false;
var messages = [];
$('.carousel').carousel({
    interval: 2000
  })
var openButton =  document.querySelector('.chatbox_button');
var chatBox =  document.querySelector('.chatbox_container');
var sendButton = document.querySelector('.btnSend');
openButton.addEventListener('click', () => toggleChatbot(chatBox))
sendButton.addEventListener('click', () => onSendBtn(chatBox))
const node = chatBox.querySelector('input');
node.addEventListener("keyup", ({key}) => {
    if (key === "Enter") {
        onSendBtn(chatBox)
    }
})

let toggleChatbot = (chatbox) => {
    state = !state;
    // show or hides the box
    if(state) {
        chatbox.classList.add('chatbox--active')
    } else {
        chatbox.classList.remove('chatbox--active')
    }
}

let onSendBtn = (chatbox) => {
    var textField = chatbox.querySelector('input');
    let txtInput = textField.value
    if (txtInput === "") {
        return;
    }
    let msgIn = { name: "User", message: txtInput }
    messages.push(msgIn);

    fetch('http://127.0.0.1:5000/reply', {
        method: 'POST',
        body: JSON.stringify({ message: txtInput }),
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json'
        },
      })
      .then(r => r.json())
      .then(r => {
        let msgResponse = { name: "Student", message: r.response };
        messages.push(msgResponse);
        updateTextBox(chatbox)
        textField.value = ''

    }).catch((error) => {
        console.error('Error:', error);
        updateTextBox(chatbox)
        textField.value = ''
      });
}

let updateTextBox = (chatbox) => {
    var html = '';
    messages.slice().reverse().forEach(function(item, index) {
        if (item.name === "Student")
        {
            html += '<div class="messages_item messages_item--student">' + (item.message)+ '</div>'
        }
        else
        {
            html += '<div class="messages_item messages_item--bot">' + (item.message) + '</div>'
        }
      });

    const chatmessage = chatbox.querySelector('.messagesBox');
    chatmessage.innerHTML = html.replaceAll('\n','<br />')
}
