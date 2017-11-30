$(document).ready(function () {

    var myPlaylist = new jPlayerPlaylist({
        jPlayer: "#jplayer_N",
        cssSelectorAncestor: "#jp_container_N"
    }, [
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
    ], {
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
        var $this = $(e.target);
        if (!$this.is('a')) $this = $this.closest('a');



        $('.jp-play-me').not($this).removeClass('active');
        $('.jp-play-me').parent('li').not($this.parent('li')).removeClass('active');

        $this.toggleClass('active');
        $this.parent('li').toggleClass('active');
        if (!$this.hasClass('active')) {
            myPlaylist.pause();

        }

        myPlaylist.add({
                title: "Your Face",
                artist: "The Stark Palace",
                mp3: "http://www.jplayer.org/audio/mp3/TSP-05-Your_face.mp3"
            });
        myPlaylist.play(-1);

    });


    // video

    $("#jplayer_1").jPlayer({
        ready: function () {
            $(this).jPlayer("setMedia", {
                title: "Big Buck Bunny",
                m4v: "http://flatfull.com/themes/assets/video/big_buck_bunny_trailer.m4v",
                ogv: "http://flatfull.com/themes/assets/video/big_buck_bunny_trailer.ogv",
                webmv: "http://flatfull.com/themes/assets/video/big_buck_bunny_trailer.webm",
                poster: "images/m41.jpg"
            });
        },
        swfPath: "js",
        supplied: "webmv, ogv, m4v",
        size: {
            width: "100%",
            height: "auto",
            cssClass: "jp-video-360p"
        },
        globalVolume: true,
        smoothPlayBar: true,
        keyEnabled: true
    });

});


