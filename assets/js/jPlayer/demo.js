+function ($) {
    $(document).ready(function () {

        var myPlaylist = new jPlayerPlaylist({
            jPlayer: "#jplayer_N",
            cssSelectorAncestor: "#jp_container_N"
        }, [
            {
                title: "Bubble",
                artist: "Miaow",
                mp3: "http://flatfull.com/themes/assets/musics/Miaow-07-Bubble.mp3",
                poster: "images/m0.jpg"
            },
            {
                title: "Lentement",
                artist: "Miaow",
                mp3: "http://flatfull.com/themes/assets/musics/Miaow-07-Bubble.mp3",
                poster: "images/m0.jpg"
            }
        ], {
            playlistOptions: {
                enableRemoveControls: true,
                autoPlay: false
            },
            swfPath: "js/jPlayer",
            supplied: "webmv, ogv, m4v, oga, mp3",
            smoothPlayBar: true,
            keyEnabled: true,
            audioFullScreen: true
        });

        $(document).on($.jPlayer.event.pause, myPlaylist.cssSelector.jPlayer, function () {
            $('.musicbar').removeClass('animate');
            $('.jp-play-me').removeClass('active');
            $('.jp-play-me').parent('li').removeClass('active');
        });

        $(document).on($.jPlayer.event.play, myPlaylist.cssSelector.jPlayer, function () {
            $('.musicbar').addClass('animate');
        });

        $(document).on('click', '.play-me', function (e) {
            e.stopPropagation();
            myPlaylist.add({
                title: "Your Face",
                artist: "The Stark Palace",
                mp3: "http://www.jplayer.org/audio/mp3/TSP-05-Your_face.mp3",
                oga: "http://www.jplayer.org/audio/ogg/TSP-05-Your_face.ogg",
                poster: "http://www.jplayer.org/audio/poster/The_Stark_Palace_640x360.png"
            });
            if ($(this).hasClass('active')) {
                player.pause();
                updateDisplay();
                return;
            }
            var id = $(this).attr("data-id");
            var i = inObj(id, playlist);
            if (i == -1) {
                $.ajax({
                    type: "get",
                    dataType: "json",
                    url: "/getsong/",
                    data: {action: "get_media", id: id},
                    async: false,
                    success: function (obj) {
                        if (obj.length == 1) {
                            player.add(obj['title']);
                            console.log(obj);
                            player.play(-1);

                            // updatePlaylist();
                        } else if (obj.length > 1) {
                            player.setPlaylist(obj);
                            player.play(0);
                            // updatePlaylist();
                        }
                    }
                });
            } else {
                if (player.current == i) {
                    setting.play ? player.pause() : player.play();
                } else {
                    player.play(i);
                }
            }
        });

        function updateDisplay() {
            $('.play-me').removeClass('active');
            $('.play-me').parent().parent().removeClass('active');
            if (playlist[player.current]) {
                var current = $('a[data-id=' + playlist[player.current]['id'] + ']' + ', ' + 'a[data-id=' + playlist[player.current]['ids'] + ']');
                if (setting.play) {
                    current.addClass('active');
                    current.parent().parent().addClass('active');
                } else {
                    current.removeClass('active');
                    current.parent().parent().removeClass('active');
                }
            }
        }

        $(document).on("pjaxEnd", function () {
            updateDisplay();
        });


        // update playlist
        function updatePlaylist() {
            updateDisplay();
            playlist = player.playlist;
            storage.set('playlist', playlist);
        }

        // check exist
        function inObj(id, list) {
            var i;
            for (i = 0; i < list.length; i++) {
                if ((list[i]['id'] == id) || (list[i]['ids'] == id)) {
                    return i;
                }
            }
            return -1;
        }


    });
}(jQuery);