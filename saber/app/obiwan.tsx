import { ResizeMode, Video } from 'expo-av';

export default function ObiWanScreen() {
    return (
        <Video
            source={require('../assets/full_video.mp4')}
            useNativeControls
            resizeMode={ResizeMode.CONTAIN}
            shouldPlay
            style={{ width: '100%', height: 300 }}
        />
    );
}