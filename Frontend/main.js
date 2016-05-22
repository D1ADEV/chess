var isDragging = false;
var oldPos = [-1, -1];
var playerTurn = -1; // Tour auquel le joueur peut jouer
var turn = -1; // Tour en cours
var url = -1;
var id = -1;
var ready = false;
var game = {};
var host = "http://localhost:8000";
var refreshInterval = 3000;

/*
DONE 
Fonction qui gère les clicks sur l'échiquier. 
Args : x et y de la pièce sur l'échiquier
Return - Callback : Aucun.
*/
var processClick = function (x, y) {
    if (ready === true && playerTurn === turn) {
        if (isDragging === false) {
            console.log('dragging');
            oldPos = [x, y];
            isDragging = true;
        } else {
            if (oldPos[0] != x || oldPos[1] != y) {
                console.log('sending');
                sendMove(oldPos[0], oldPos[1], x, y);
            } else {
                console.log('canceling');
                isDragging = false;
                oldPos = [-1, -1];
            }
        }
    } else {
        alert('The game isn\'t ready / Not your turn');
    }
};


/*
DONE
Fonction qui renvoie l'index dans le tableau de jeu d'une pièce 
en fonction de ses coordonnées
Args : x et y de la pièce
Return - Callback : Index de la pièce.
*/
var getIndexFromPosition = function (x, y) {
    if (y == 1) {
        return x - 1;
    } else {
        return ((((y - 1) * 8) + x) - 1);
    }
};

/*
DONE
Fonction qui envoie le mouvement au serveur
Args : x, y de la pièce qui va bouger et x, y de la destination
Return - Callback : Aucun
*/

var sendMove = function (oldX, oldY, x, y) {
    var array = {
        'oldX': oldX,
        'oldY': oldY,
        'x': x,
        'y': y,
        'id': id
    };
    console.log(array);
    $.post(host + '/move/' + url + '/' + id, {
        'move': JSON.stringify(array)
    }, function (data) {
        console.log(data);
    }).done(function (data) {
        var resp = JSON.parse(data);
        if (resp.error !== undefined) {
            alert(resp.error);
        } else {
            game = JSON.parse(data);
            $("#b").trigger("render");
        }
    });
    isDragging = false;
};


/*
Fonctions utilisant jquery. Ne sont pas accessibles depuis le DOM
*/

$(function () {
    /*
    ONLY FUNCTIONS THAT MATTER
    */

    /*
    DONE
    Fonction qui crée et join un nouvelle partie
    Args : Aucun
    Return - Callback : Aucun
    */
    var createAndJoinGame = function () {
        create(function () {
            join(function () {
                console.log('id : ' + id + ' url : ' + url);
                getGameState(function (data) {
                    refresh(data, function () {
                        var int = setInterval(function () {
                            if (game.winner == -1) {
                                getGameState(function (temp) {
                                    refresh(temp);
                                });
                            } else {
                                clearInterval(int);
                                return;
                            }
                        }, refreshInterval);
                    });
                });
            });
        });
    };

    /*
    DONE
    Fonction qui join une partie existante
    Args : url de partie
    Return - Callback : Aucun
    */
    var joinExistingGame = function (uniqueurl) {
        url = uniqueurl;
        join(function () {
            console.log('id : ' + id + ' url : ' + url);
            getGameState(function (data) {
                refresh(data, function () {
                    setInterval(function () {
                        getGameState(function (temp) {
                            refresh(temp);
                        });
                    }, refreshInterval);
                });
            });
        });
    };


    /*
    Réagit au click sur le bouton de join
    */
    $('#join').click(function () {
        joinExistingGame($('#idInput').val());
    });

    /*
    Réagit au click sur le bouton de création
    */
    $('#create').click(function () {
        createAndJoinGame();
    });

    $("#b").on("render", function () {
        console.log('ok got something');
        console.log(game);
        flushHtml();
        render();
    });

    /*
    THESE FUNCTIONS ARE 'PRIVATE', AND SHOULDNT BE CALLED
    */


    /*
    DONE
    Fonction qui crée un nouvelle partie
    Args : Callback facultatif
    Return - Callback : Si un callback est donné en paramètres, il est appelé. 
    */
    var create = function (cb) {
        $.ajax(host + '/createnewgame').done(function (data) {
            if (data != 'False') {
                var parsed = JSON.parse(data);
                url = parsed.uniqueurl;
                cb();
            } else {
                console.log('wtf');
            }
        });
    };

    /*
    DONE
    Fonction qui join une partie
    Args : Callback 
    Return : Callback
    */
    var join = function (cb) {
        $.ajax(host + '/joingame/' + url).done(function (data) {
            if (data != 'False') {
                var parsed = JSON.parse(data);
                id = parsed.id;
                playerTurn = parsed.turn;
                cb();
            } else {
                console.log('wtf2');
            }
        });
    };

    /*
    DONE
    Fonction qui affiche l'échiquier
    Args : Aucun
    Return - Callback : Aucun
    */
    var render = function () {
        var html = '';
        html += ' <div id="chessTable"> <table id="e"> <thead> <tr> <th> </th> <th> 1</th> <th> 2 </th> <th> 3 </th> <th> 4 </th> <th> 5 </th> <th> 6 </th> <th> 7 </th> <th> 8 </th> </tr> </thead> <tbody> ';

        var x = 1;
        var y = 1;
        for (var i = 0; i < game.board.length; i++) {
            if (x > 8) {
                html += '</tr>';
                x = 1;
                y++;
            }
            if (x == 1) {
                html += '<tr><td class="num">' + y + '</td>';
            }
            //html += '<td onclick="processClick(' + x + ', ' + y + ');"><img src="assets/roi32x32noir.png"></td>';
            var index = getIndexFromPosition(y, x);
            if (game.board[index][0] != 'E') {
                if (game.board[index][1] === 0) {
                    html += '<td class="white" onclick="processClick(' + x + ', ' + y + ');">' + getChar(game.board[index][0])+ '</td>'; // (y, x) et pas (x, y). Pourquoi? Je ne sais pas. Mais ça march    
                } else {
                    html += '<td class="black" onclick="processClick(' + x + ', ' + y + ');">' + getChar(game.board[index][0]) + '</td>'; // (y, x) et pas (x, y). Pourquoi? Je ne sais pas. Mais ça march    
                }

            } else {
                html += '<td onclick="processClick(' + x + ', ' + y + ');"></td>';
            }
            x++;
        }
        html += '</tbody></table></div>';
        $('#b').append(html);
    };
    
    var getChar = function(piece, player){
        if(player == 1){
            switch(piece){
                case "K":
                    return "&#9812;";
                case "Kn":
                    return "&#9816;";
                case "P":
                    return "&#9817;";
                case "B":
                    return "&#9815;";
                case "R":
                    return "&#9814;";
                case "Kn":
                    return "&#9816;";
                case "Q":
                    return "&#9813;";
                case "E":
                    return " ";
            }
        } 
        else {
            switch(piece){
                case "K":
                    return "&#9818;";
                case "Kn":
                    return "&#9822;";
                case "P":
                    return "&#9823;";
                case "B":
                    return "&#9821;";
                case "R":
                    return "&#9820;";
                case "Kn":
                    return "&#9822;";
                case "Q":
                    return "&#9819;";
                case "E":
                    return " ";
            }
            
        }
    }


    /*
    DONE 
    Fonction qui récupère l'état de la partie depuis le serveur
    Args : Callack
    Return - Callback : Callback avec Objet javascript parsé du JSON renvoyé 
    par le seveur
    */
    var getGameState = function (cb) {
        console.log('getting game state');
        $.ajax(host + '/gameupdate/' + url).done(function (data) {
            console.log(JSON.parse(data));
            cb(JSON.parse(data));
        });
    };

    /*
    DONE
    Fonction qui vide le body pour mise à jour de l'échiquier
    Args : Aucun
    Return - Callback : Aucun
    */
    var flushHtml = function () {
        $("#b").empty();
    };

    /*
    DONE
    Fonction qui met à jour la partie en local
    Args : Nouveau objet représentant la partie, Callback
    Return - Callback : Callback
    */
    var refresh = function (newB, cb) { // cb is optional, not using it in the main setInterval
        if (newB.board != game.board) {
            game = newB;
            turn = game.playerTurn;
            if (game.checkmate == true) {
                if (game.winner == playerTurn) {
                    alert('You won!');
                    cb();
                } else {
                    alert('You lost!');
                    cb();
                }
            }
            flushHtml();
            render();
            if (cb !== undefined) { // Only calling the cb if it is needed
                cb();
            }
        } else {
            console.log('same');
            if (cb !== undefined) { // Same 
                cb();
            }
        }
        ready = game.ready;
    };
});