document.addEventListener('DOMContentLoaded', function () {
     // Delete Comment Functionality
    document.querySelectorAll('.delete-comment-btn').forEach(button => {
        button.addEventListener('click', function () {
            const commentId = this.dataset.commentId;
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            if (confirm('Are you sure you want to delete this comment?')) {
                fetch(`/delete_comment/${commentId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        document.getElementById(`comment-${commentId}`).remove();
                    }
                });
            }
        });
    });
});
