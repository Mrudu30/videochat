// Basic info for the video user
const APP_ID = "cf8338f00b7842788c354fce4fd390c7"
const CHANNEL_NAME ='main'
const TOKEN = '007eJxTYKhK1hSadbLk3stysVU+DH0dFtsDfPomBac91TF7cUjnxU4FhuQ0C2NjizQDgyRzCxMjcwuLZGNTk7TkVJO0FGNLg2RzPe0JqQ2BjAyVO3YzMjJAIIjPwpCbmJnHwAAAHpQe4g=='

let UID;

const client = AgoraRTC.createClient({mode:'rtc', codec:'vp8'})

let localTracks = []
let remoteUsers = {}

let joinAndDisplayLocalStream = async() =>{

    client.on('user-published', handleJoinedUser)

    // user id creation
    UID = await client.join(APP_ID, CHANNEL_NAME, TOKEN, null)

    // creates local tracks and add value in list
    localTracks = await AgoraRTC.createMicrophoneAndCameraTracks()

    // dynamic player that adds a user in this frame to the html
    let player = `<div class="video-container" id="user-container-${UID}">
                    <div class="username-wrapper"><span class="user-name">My name</span></div>
                    <div class="video-player" id="user-${UID}"></div>
                </div>`
           
    document.getElementById('video-streams').insertAdjacentHTML('beforeend',player) 
    
    // play the video track and play it 
    localTracks[1].play(`user-${UID}`)

    // publish audio and video to channel
    await client.publish([localTracks[0], localTracks[1]])
}

let handleJoinedUser = async(user, mediaType) =>{
    remoteUsers[user.uid] = user
    await client.subscribe(user,mediaType)

    if(mediaType === 'video'){
        let player = document.getElementById(`user-container-${user.uid}`)
        if (player != null){
            player.remove()
        }

        player = `<div class="video-container" id="user-container-${user.uid}">
                    <div class="username-wrapper"><span class="user-name">My name</span></div>
                    <div class="video-player" id="user-${user.uid}"></div>
                </div>`
           
        document.getElementById('video-streams').insertAdjacentHTML('beforeend',player)
        user.videoTrack.play(`user-${UID}`)
    }

    if (mediaType === 'audio')
    {
        user.audioTrack.play()
    }
}

joinAndDisplayLocalStream()