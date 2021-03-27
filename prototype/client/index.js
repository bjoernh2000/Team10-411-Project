let submitAPIButton = document.getElementById("submit_api");

submitAPIButton.onclick = function() {
    console.log("send API request to backend to process");
    let content = document.getElementById("API_call_field").value;
    console.log(content);
    
    let endpoint = "http://127.0.0.1:4000/postAPI";

    let formData = new FormData();
    formData.append('APICall', content);
    console.log(formData);
    axios.post(endpoint, formData, {headers : {
        'Content-Type': 'multipart/form-data'
    }})
        .then((res) => {
            console.log(res);
            alert("Sucessfully sent to backend")
        })
        .catch((err) => {
            console.error(err);
            alert("Error: " + err.message)
        })

}