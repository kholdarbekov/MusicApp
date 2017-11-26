$(document).ready(function(){
    var cssSelector = {
        jPlayer: "#jplayer_N",
        cssSelectorAncestor: "#jp_container_N"
    };

    var playlist = [];

    var options = {
        playlistOptions: {
            enableRemoveControls: true,
            autoPlay: true
        },
        swfPath: "js/jPlayer",
        supplied: "webmv, ogv, m4v, oga, mp3",
        smoothPlayBar: true,
        keyEnabled: true,
        audioFullScreen: false
    };

    var myPlaylist = null;

    function loadSong(){
        var song_artist = findArtist();
        var song_title = findTitle();
        var song_poster = findPoster();      

        if(myPlaylist == null)
            myPlaylist = new jPlayerPlaylist(cssSelector, playlist, options);

        myPlaylist.add({
            title: song_title,
            artist: song_artist,
            oga: sessionStorage.getItem("file_url"),
            poster: song_poster
        });

        $(document).on($.jPlayer.event.pause, myPlaylist.cssSelector.jPlayer,  function(){
            $('.musicbar').removeClass('animate');
            $('.jp-play-me').removeClass('active');
            $('.jp-play-me').parent('li').removeClass('active');
        });

        $(document).on($.jPlayer.event.play, myPlaylist.cssSelector.jPlayer,  function(){
            $('.musicbar').addClass('animate');
        });

        $(document).on('click', '.jp-play-me', function(e){
            e && e.preventDefault();
            var $this = $(e.target);
            if (!$this.is('a')) $this = $this.closest('a');

            $('.jp-play-me').not($this).removeClass('active');
            $('.jp-play-me').parent('li').not($this.parent('li')).removeClass('active');

            $this.toggleClass('active');
            $this.parent('li').toggleClass('active');
            if( !$this.hasClass('active') ){
                myPlaylist.pause();
            }else{
                var i = Math.floor(Math.random() * (1 + 7 - 1));
                myPlaylist.play(i);
            }
        });
    }    
});