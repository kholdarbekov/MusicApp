$(document).ready(function () {
    var playlist = [];
    var myPlaylist = new jPlayerPlaylist({
            jPlayer: "#jplayer_N",
            cssSelectorAncestor: "#jp_container_N"
        },
        playlist
        ,
        {
            playlistOptions: {
                enableRemoveControls: true,
                autoPlay: false
            },
            swfPath: "js/jPlayer",
            supplied: "webmv, ogv, m4v, oga, mp3",
            smoothPlayBar: true,
            keyEnabled: true,
            audioFullScreen: false
        });

    myPlaylist.setPlaylist([
        {
            title: "Cro Magnon Man",
            artist: "The Stark Palace",
            mp3: "http://www.jplayer.org/audio/mp3/TSP-01-Cro_magnon_man.mp3",
        },
        {
            title: "Hidden",
            artist: "Miaow",
            mp3: "http://www.jplayer.org/audio/mp3/Miaow-02-Hidden.mp3",
        }
    ]);

    $(document).on($.jPlayer.event.pause, myPlaylist.cssSelector.jPlayer, function () {
        $('.musicbar').removeClass('animate');
        $('.jp-play-me').removeClass('active');
        $('.jp-play-me').parent('li').removeClass('active');
    });

    $(document).on($.jPlayer.event.play, myPlaylist.cssSelector.jPlayer, function () {
        $('.musicbar').addClass('animate');
    });

    $(document).on('click', '.jp-play-me', function (e) {
        e.stopPropagation();


        if (!$(this).hasClass('active')) {
            myPlaylist.pause();
            return;
        }

        var id = $(this).data('id');
        var i = inObj(id, playlist);
        if (i == -1) {
            $.ajax({
                type: "get",
                dataType: "json",
                url: "/getsong/",
                data: {action: "get_media", id: id},
                success: function (obj) {
                    myPlaylist.add(obj);
                    myPlaylist.play(-1);
                    updatePlaylist();
                    // alert(playlist.length);
                }
            });
        }
        else {
            if (myPlaylist.current == i) {
                myPlaylist.play();
                // updateDisplay()
            } else {
                myPlaylist.play(i);
                // updateDisplay()
            }
        }

    });


    // function updateDisplay() {
    //     $('.jp-play-me').removeClass('active');
    //     $('.jp-play-me').parent().parent().removeClass('active');
    //     myPlaylist.current.addClass('active');
    //     myPlaylist.current.parent().parent().addClass('active');
    // }

    function updatePlaylist() {
        // updateDisplay();
        playlist = myPlaylist.playlist;
    }

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


