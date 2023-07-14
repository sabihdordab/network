document.addEventListener( 'DOMContentLoaded',function() {

    document.querySelector('#submit').disabled = true;

    document.querySelector('#post-content').onkeyup = function(){

        if (document.querySelector('#post-content').value.trim()){

            document.querySelector('#submit').disabled = false;
        }
        else{
            document.querySelector('#submit').disabled = true;
        }
    }
})


function editPost(postId){
    let postDiv = document.querySelector(`#post-${postId}`);
    let title = document.querySelector(`#post-title-${postId}`);
    let content = document.querySelector(`#post-content-${postId}`);
    let input = document.createElement('INPUT');
    let textArea = document.createElement('textarea');
    let submitBTN = document.createElement('button');
    let br = document.createElement('br');
    let div = document.createElement('div');
    const titleLBL = document.createElement('label');
    const contentLBL = document.createElement('label');
    titleLBL.innerHTML = "New Title :";
    contentLBL.innerHTML = "New Content :";

    input.setAttribute("type", "text");
    textArea.className = 'form-control';
    input.className = 'form-control';
    input.id = `edited-post-title-${postId}`;
    textArea.id = `edited-post-content-${postId}`;
    input.value = title.innerHTML;
    textArea.value = content.innerHTML;
    textArea.style.width = '100%';
    title.style.width = '100%';
    submitBTN.innerHTML = "Submit" ;
    submitBTN.className = 'btn btn-primary';
    div.className = 'container';

    div.appendChild(titleLBL);
    div.appendChild(input);
    div.appendChild(contentLBL);
    div.appendChild(textArea);
    div.appendChild(br);
    div.appendChild(submitBTN);
    postDiv.appendChild(div)

    submitBTN.addEventListener('click' , function(){
        if (!document.querySelector(`#edited-post-content-${postId}`).value.trim()) {
            alert("Post content can't be None");
            return;
        }
        fetch(`/edit/${postId}`,{
            method : "POST",
            body: JSON.stringify({
                editedTitle : document.querySelector(`#edited-post-title-${postId}`).value,
                editedContent: document.querySelector(`#edited-post-content-${postId}`).value 
            })
        })
        .then(response => response.json())
        .then(result => {
            title.innerHTML = result.title;
            content.innerHTML = result.content;

            postDiv.removeChild(div);
        })
    });

}


function likePost(postId){
    fetch(`/like/${postId}`, {
        method: "POST"
    })
    .then(response => response.json())
    .then(result => {
        if (result.message == 'failed'){
            alert("Please Login");
            return;
        }

        if(result.is_liked){
            document.querySelector(`#like-btn-${postId}`).innerHTML = "UnLike"
        }
        else
        {
            document.querySelector(`#like-btn-${postId}`).innerHTML = "Like"
        }
        
        document.querySelector(`#post-${postId}-likes`).innerHTML = `likes: ${result.likes}`;
    })
}