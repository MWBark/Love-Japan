const commentEditButtons = document.getElementsByClassName("btn-edit");
const commentText = document.getElementById("id_body");
const commentForm = document.getElementById("imageCommentForm");
const submitButton = document.getElementById("submitButton");

const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
const deleteTitle = document.getElementById("deleteModalLabel")
const deleteBody = document.getElementById("delete-message")
const deleteCommentButtons = document.getElementsByClassName("btn-comment-delete");
const deleteImageButton = document.getElementById("image-delete")
const deleteConfirm = document.getElementById("deleteConfirm");

/**
* Initializes edit functionality for the provided comment edit buttons.
* 
* For each button in the `commentEditButtons` collection:
* - Retrieves the associated comment's ID upon click.
* - Fetches the content of the corresponding comment.
* - Populates the `commentText` input/textarea with the comment's content for editing.
* - Updates the submit button's text to "Update".
* - Sets the form's action attribute to the `edit_comment/{commentId}` endpoint.
*/
for (let button of commentEditButtons) {
  button.addEventListener("click", (e) => {
    let commentId = e.target.getAttribute("data-comment_id");
    let commentContent = document.getElementById(`comment${commentId}`).innerText;
    commentText.value = commentContent;
    submitButton.innerText = "Update";
    commentForm.setAttribute("action", `edit_comment/${commentId}`);
  });
}

/**
* Initializes deletion functionality for 
* the provided delete comment buttons.
* 
* For each button in the `deleteCommentButtons` collection:
* - Retrieves the associated comment's ID upon click.
* - Inserts text into the title and body of
* a confirmation modal (`deleteCommentModal`)
* - Updates the `deleteConfirm` link's href to point to the 
* deletion endpoint for the specific comment.
* - Displays the confirmation modal to prompt 
* the user for confirmation before deletion.
*/
for (let button of deleteCommentButtons) {
  button.addEventListener("click", (e) => {
    let commentId = e.target.getAttribute("data-comment_id");
    deleteTitle.innerText = "Delete Comment?";
    deleteBody.innerText = `
      Are you sure you want to delete your comment?
      This action cannot be undone.
    `;
    deleteConfirm.href = `delete_comment/${commentId}`;
    deleteModal.show();
  });
}

/**
 * Initializes deletion functionality for
 * image delete button by:
 * 
 * - Inserting text into the title and body of
 * a confirmation modal (`deleteCommentModal`)
 * - Updates the `deleteConfirm` link's href
 * to 'delete_post' url
 * - Displays the confirmation modal to prompt 
 * the user for confirmation before deletion.
 */
deleteImageButton.addEventListener("click", (e) => {
  deleteTitle.innerText = "Delete Image?";
  deleteBody.innerText = `
    Are you sure you want to delete this image?
    This action cannot be undone.
  `;
  deleteConfirm.href = "delete_post";
  deleteModal.show();
});
