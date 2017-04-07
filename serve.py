from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Piece

app = Flask(__name__)

engine = create_engine('sqlite:///civicart.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/feed/JSON')
def feedJSON():
    feed = session.query(Piece).all()
    return jsonify(feed=[piece.serialize for piece in feed])

@app.route('/feed/<int:piece_id>/JSON')
def pieceJSON():
    pass

# Show entire feed
@app.route('/')
@app.route('/feed/')
def showFeed():
    feed = session.query(Piece).all()
    return render_template('feed.html', feed=feed)


# Create a new piece
@app.route('/feed/new/', methods=['GET', 'POST'])
def newPiece():
    if request.method == 'POST':
        newPiece = Piece(
            title=request.form['title'],
            description=request.form['description'], 
            latitude=request.form['latitude'],
            longitude=request.form['longitude'],
            img_url=request.form['img_url']
        )
        session.add(newPiece)
        session.commit()
        return redirect(url_for('showFeed'))
    else:
        return render_template('newPiece.html')

# Edit a piece
@app.route('/feed/<int:piece_id>/edit/', methods=['GET', 'POST'])
def editPiece(piece_id):
    editedPiece = session.query(
        Piece).filter_by(id=piece_id).one()
    if request.method == 'POST':
        print(request.form['title'])
        if request.form['title']:
            editedPiece.title = request.form['title']
            editedPiece.description = request.form['description']
            editedPiece.latitude = request.form['latitude']
            editedPiece.longitude = request.form['longitude']
            editedPiece.img_url = request.form['img_url']
            return redirect(url_for('showFeed'))
        else: 
            return redirect(url_for('showFeed'))
    else:
        return render_template(
            'editPiece.html', piece=editedPiece)

# Delete a piece
@app.route('/feed/<int:piece_id>/delete/', methods=['GET', 'POST'])
def deletePiece(piece_id):
    pieceToDelete = session.query(
        Piece).filter_by(id=piece_id).one()
    if request.method == 'POST':
        session.delete(pieceToDelete)
        session.commit()
        return redirect(url_for('showFeed'))
    else:
        return render_template(
            'deletePiece.html', piece=pieceToDelete)

# Show piece 
@app.route('/feed/<int:piece_id>/')
def showPiece(piece_id):
    piece = session.query(Piece).filter_by(id=piece_id).one()
    return render_template('piece.html', piece=piece)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=3000)
