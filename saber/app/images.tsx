import { FlatList, Image } from 'react-native';

export default function ImagesScreen() {
    const images = []; // fetch from backend later

    return (
        <FlatList
            data={images}
            keyExtractor={(item) => item.id}
            renderItem={({ item }) => (
                <Image
                    source={{ uri: item.url }}
                    style={{ width: 300, height: 300 }}
                />
            )}
        />
    );
}