from flask import (Blueprint, request, jsonify)
from app.models.models import (db, comments)
from app.services.jwt_service import (decode)
from app.services.auth_service import (comment)

subcomment_bp = Blueprint("submit_comment", __name__)

@subcomment_bp.route("/post-comments", methods=["POST"])
def Comments():

    comments_header = request.headers.get("Authorization")
    if not comments_header:
        return jsonify({"error": "No Authorization header"}), 401

    try:
        comment_token = comments_header.split(" ")[1]

        data = decode(comment_token)

        # Access the payload keys directly
        # username = data["username"]
        user_id = data["user-id"]

        input, article = comment()

        # print(article)

        userComments = comments(
            user_comments=input, user_id=user_id, article_url=article
        )
        print(vars(userComments))

        db.session.add(userComments)
        db.session.commit()
        '''
        print(userComments.id)
        print(userComments.author.username)
        print(userComments.user_comments)
        print(userComments.article_url)
        '''
        saved_comment = comments.query.filter_by(id=userComments.id).first()

        return jsonify({"username": saved_comment.author.username, "user_comment": saved_comment.user_comments, "timestamp": saved_comment.timestamp})

    except Exception as e:
        print(str(e))
        return jsonify({"error": str(e)}), 400