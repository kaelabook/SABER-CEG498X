import { Stack } from "expo-router";

export default function Layout() {
  return ( 
    <Stack>
      <Stack.Screen name="index" options={{ title: 'Message' }} />
      <Stack.Screen name="images" options={{ title: 'Weakness Images' }} />
      <Stack.Screen name="login" options={{ title: 'Authentication' }} />
      <Stack.Screen name="obiwan" options={{ title: 'Obi-Wan Only' }} />

    </Stack>
  );
}
