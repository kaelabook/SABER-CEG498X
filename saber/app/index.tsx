import { Text, Button } from "react-native";
import { useRouter } from 'expo-router';
import { View, StyleSheet } from 'react-native'
import { ResizeMode, Video } from 'expo-av';

export default function HomeScreen() {
  const router = useRouter();

  return (
    <>
      <Text>Incoming Rebel Transmission...</Text>

      <View style={styles.container}>
        <Video
          source={require('../assets/intro.mp4')}
          style={styles.video}
          useNativeControls
          resizeMode={ResizeMode.CONTAIN}
          shouldPlay
        />
      </View>

      <Button title="View Images" onPress={() => router.push('/images')} />
      <Button title="Authenticate" onPress={() => router.push('/login')} />
    </>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
  },
  video: {
    width: '100%',
    height: 250,
  },
});
