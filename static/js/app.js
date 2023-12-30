const messages = document.getElementById("messages");
const close = document.getElementById("close");

if (messages) {
  close.addEventListener("click", function () {
    messages.style.display = "none";
  });
}

const postLikeUrl = "/blog/like/";
const commentUrl = "/blog/comment/";
const followUrl = "/account/follow/";
const likeButton = document.querySelector("a.like");
const commentForm = document.getElementsByName("comment-form")[0];
const followButton = document.querySelector("a.follow");
const csrftoken = Cookies.get("csrftoken");

const options = {
  method: "POST",
  headers: { "X-CSRFToken": csrftoken },
  mode: "same-origin",
};

if (likeButton) {
  likeButton.addEventListener("click", function (e) {
    e.preventDefault();
    if (!likeButton.classList.contains("disabled")) {
      const form = new FormData();
      form.append("id", likeButton.dataset.id);
      form.append("action", likeButton.dataset.action);
      options["body"] = form;
      fetch(postLikeUrl, options)
        .then((response) => response.json())
        .then((data) => {
          console.log(data);
          if (data["status"] === "ok") {
            const performedAction = likeButton.dataset.action;
            const likesCount = document.querySelector("span.likes-count");
            const likes = Number.parseInt(likesCount.innerHTML);
            likesCount.innerHTML =
              performedAction === "like" ? likes + 1 : likes - 1;
            likeButton.dataset.action =
              performedAction === "like" ? "unlike" : "like";
          }
        });
    }
  });
}

if (commentForm) {
  commentForm.addEventListener("submit", function (e) {
    e.preventDefault();
    const commentBody = document.querySelector("textarea[name=comment-body]");
    if (commentBody.value !== "") {
      const form = new FormData();
      form.append("id", commentForm.dataset.id);
      form.append("body", commentBody.value);
      options["body"] = form;
      fetch(commentUrl, options)
        .then((response) => response.json())
        .then((data) => {
          if (data["status"] === "ok") {
            commentBody.innerHTML = "";
            const comments = document.getElementById("comments");
            const comment = document.createElement("div");
            comment.className = "comment";
            const author = document.createElement("p");
            author.className = "author";
            author.appendChild(document.createTextNode(data["author"]));
            const date = document.createElement("span");
            date.className = "date";
            date.appendChild(
              document.createTextNode(formateDate(data["created_at"])),
            );
            const message = document.createElement("p");

            message.appendChild(document.createTextNode(data["body"]));
            comment.appendChild(author);
            comment.appendChild(date);
            comment.appendChild(message);
            comments.append(comment);
          }
        });
    }
  });
}

if (followButton) {
  followButton.addEventListener("click", function (e) {
    e.preventDefault();
    const form = new FormData();
    form.append("id", followButton.dataset.id);
    form.append("action", followButton.dataset.action);
    options["body"] = form;
    fetch(followUrl, options)
      .then((response) => response.json())
      .then((data) => {
        if (data["status"] === "ok") {
          const performedAction = followButton.dataset.action;
          const nextAction =
            performedAction === "follow" ? "unfollow" : "follow";
          followButton.innerHTML =
            nextAction[0].toUpperCase() + nextAction.slice(1);
          followButton.dataset.action = nextAction;
          const followersCount = document.querySelector("span.count .total");
          const totalCount = Number.parseInt(followersCount.innerHTML);
          followersCount.innerHTML =
            performedAction === "follow" ? totalCount + 1 : totalCount - 1;
        }
      });
  });
}

const formateDate = (date) => {
  const options = {
    month: "short",
    day: "numeric",
    year: "numeric",
    hour: "numeric",
    minute: "numeric",
    hour12: true,
  };
  return Intl.DateTimeFormat("en-us", options).format(new Date(date));
};
