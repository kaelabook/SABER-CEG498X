import { Button, TextInput } from 'react-native';
import { useRouter } from 'expo-router';


export default function LoginScreen() {
    const router = useRouter();

    function authenticate() {
        // placeholder auth logic
        router.replace('/obiwan');
    }

    return (
        <>
            <TextInput placeholder="Username" />
            <TextInput placeholder="Password" secureTextEntry />
            <Button title="Authenticate" onPress={authenticate} />
        </>
    );
}

