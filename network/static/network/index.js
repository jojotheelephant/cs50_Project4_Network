// ~~~~ variables tied to DOM elements ~~~~
// document querySelector - used in post()
const post_body = document.querySelector("#newpost-body");
const post_message = document.querySelector("#newpost_message");

// METHODS
// read value for csrftoken
const get_csrfToken = () => {
    const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
    return csrftoken;
};

// Display Post Status Message for new_post
// 1. console.log message
// 2. clears post body
// 3. displays 'message' in innerHTML. success = green, error = red
// 4. remove 'message' after 5 seconds
const displayPostMessage = (message) => {
    console.log(message);
    post_body.value = "";
    message === "Post successful" ? (post_message.style.color = "lightgreen") : (post_message.style.color = "red");
    post_message.innerHTML = message;
    setTimeout(() => (post_message.innerHTML = ""), 5000);
};

// New post using async await
const new_post = async () => {
    body = post_body.value;
    // POST request config
    const config = {
        method: "POST",
        body: JSON.stringify({
            body: body,
        }),
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": get_csrfToken(),
            Accept: "application/json",
            "Content-Type": "application/json",
        },
    };
    // send fetch with config request using async await try catch
    try {
        const response = await fetch("/newpost", config);
        const data = await response.json();
        if (data.message) {
            displayPostMessage(data.message);
        } else if (data.error) {
            displayPostMessage(data.error);
        }
    } catch (err) {
        console.error(err);
    }
    // do not refresh page
    return false;
};

const sayHello = () => {
    console.log("Hello");
};
