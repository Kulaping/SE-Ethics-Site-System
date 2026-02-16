from flask import (Blueprint, request, jsonify)
from app.models.models import (db, comments)
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

displayComms_bp = Blueprint("display_comments", __name__)

@displayComms_bp.route("/display-comments", methods=["GET"])
def get_comments():
    article = request.args.get("article")
    print(f"test: {article}")
    outputs = []
    # idEach_comment = 0

    filtered_comments = comments.query.filter_by(article_url=article).all()

    for comment in filtered_comments:
        print(comment)
        print(comment.user_comments)

        # print(comment.user_comments)
        #  user_who_posted = Userdb.query.get(comment.user_id)
        outputs.append(
            {
                "username": comment.author.username,
                "comment": comment.user_comments,
                "timestamp": comment.timestamp.strftime("%b %d, %H:%M"),
            }
        )

    logger.info(json.dumps(outputs, indent=4))

    return jsonify(outputs)