import React from 'react';
import {
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
  TextInput,
  Button,
  KeyboardAvoidingView,
  Platform,
  TouchableWithoutFeedback,
  Keyboard,
} from 'react-native';
import { Formik } from 'formik';
import Autocomplete from 'react-native-autocomplete-input';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

const ClubSchema = Yup.object().shape({
  clubName: Yup.string().required('Required'),
  clubPassword: Yup.string().required('Required'),
});

const AttendSchema = Yup.object().shape({
  studentID: Yup.string().length(9, 'Invalid StudentID').required('Required'),
  code: Yup.string().required('Required'),
});

async function sendStudentIDandCodeToAPI(data) {
  try {
    const response = await fetch('', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    const json = await response.json();
    return json;
  } catch (error) {
    console.error(error);
  }
}

async function sendClubInfoToAPI(data) {
  try {
    const response = await fetch('', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    const json = await response.json();
    return json;
  } catch (error) {
    console.error(error);
  }
}

function clubSuccess() {
  return (
    <View>
      <Text>Club has been succesfully registered.</Text>
    </View>
  );
}

function attendSuccess() {
  return (
    <View>
      <Text>You have succesfully attended the event.</Text>
    </View>
  );
}

function clubFail({ navigation }) {
  return (
    <View>
      <Text>Sorry, try registering your club again.</Text>
      <TouchableOpacity
        onPress={() => navigation.navigate('ClubForm')}
        style={{ backgroundColor: 'blue' }}
      >
        <Text style={{ fontSize: 20, color: '#fff' }}>Go back</Text>
      </TouchableOpacity>
    </View>
  );
}

function attendFail({ navigation }) {
  return (
    <View>
      <Text>Sorry, try attending the event again.</Text>
      <TouchableOpacity
        onPress={() => navigation.navigate('AttendeeForm')}
        style={{ backgroundColor: 'blue' }}
      >
        <Text style={{ fontSize: 20, color: '#fff' }}>Go back</Text>
      </TouchableOpacity>
    </View>
  );
}

function AttendeeForm({ navigation }) {
  return (
    <Formik
      initialValues={{ studentID: '', code: '' }}
      validationSchema={AttendSchema}
      validateOnBlur
      onSubmit={async values => {
        await sendStudentIDandCodeToAPI(values).then(res => {
          if (res.status !== '201') {
            () => navigation.navigate('attendFail');
          } else {
            () => navigation.navigate('attendSuccess');
          }
        });
      }}
    >
      {({
        handleChange,
        handleBlur,
        handleSubmit,
        values,
        errors,
        touched,
      }) => (
        <KeyboardAvoidingView
          behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
          style={styles.container}
        >
          <TouchableWithoutFeedback onPress={Keyboard.dismiss}>
            <View style={styles.inner}>
              <Text style={styles.header}>Join Event</Text>
              <TextInput
                style={styles.textInput}
                onChangeText={handleChange('studentID')}
                onBlur={handleBlur('studentID')}
                value={values.studentID}
                placeholder="StudentID (1009999)"
                keyboardType="numeric"
              />
              {touched.studentID && errors.studentID && (
                <Text style={{ fontSize: 12, color: '#FF0D10' }}>
                  {errors.studentID}
                </Text>
              )}
              <TextInput
                style={styles.textInput}
                onChangeText={handleChange('code')}
                onBlur={handleBlur('code')}
                value={values.code}
                placeholder="Event Code (5782)"
                keyboardType="numeric"
              />
              {touched.code && errors.code && (
                <Text style={{ fontSize: 12, color: '#FF0D10' }}>
                  {errors.code}
                </Text>
              )}
              <View style={styles.btnContainer}>
                <Button title="Submit" onPress={handleSubmit} />
              </View>
            </View>
          </TouchableWithoutFeedback>
        </KeyboardAvoidingView>
      )}
    </Formik>
  );
}

function ClubForm({ navigation }) {
  const [allClubs, setAllClubs] = useState();
  const [query, setQuery] = useState('');
  const queriedClubs = allClubs?.query(query);
  const isLoading = !allClubs?.length;
  const placeholder = isLoading ? 'Loading data...' : 'Enter Your Club Name';

  useEffect(() => {
    (async function fetchClubs() {
      setAllClubs(await fetchClubs());
    })();
  }, []);
  return (
    <Formik
      initialValues={{ clubName: '', clubPassword: '' }}
      validationSchema={ClubSchema}
      validateOnBlur
      onSubmit={async values => {
        await sendClubInfoToAPI(values).then(res => {
          if (res.status !== '201') {
            () => navigation.navigate('clubFail');
          } else {
            () => navigation.navigate('clubSuccess');
          }
        });
      }}
    >
      {({
        handleChange,
        handleBlur,
        handleSubmit,
        values,
        isValid,
        errors,
        touched,
      }) => (
        <KeyboardAvoidingView
          behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
          style={styles.container}
        >
          <TouchableWithoutFeedback onPress={Keyboard.dismiss}>
            <View style={styles.inner}>
              <Text style={styles.header}>Register Your Club</Text>
              <Autocomplete
                editable={!isLoading}
                autoCorrect={false}
                data={
                  queriedClubs?.length === 1 &&
                  queriedClubs[0].compareTitle(query)
                    ? []
                    : queriedClubs
                }
                value={query}
                onChangeText={setQuery}
                placeholder={placeholder}
                flatListProps={{
                  keyboardShouldPersistTaps: 'always',
                  keyExtractor: club => club.id,
                  renderItem: ({ item: { clubName } }) => (
                    <TouchableOpacity onPress={() => setQuery(clubName)}>
                      <Text style={styles.itemText}>{title}</Text>
                    </TouchableOpacity>
                  ),
                }}
              />
              {/* <TextInput
                style={styles.textInput}
                onChangeText={handleChange('clubName')}
                onBlur={handleBlur('clubName')}
                value={values.clubName}
                placeholder="Club Name"
              /> */}
              <TextInput
                style={styles.textInput}
                onChangeText={handleChange('clubPassword')}
                onBlur={handleBlur('clubPassword')}
                value={values.clubPassword}
                placeholder="Club Password"
              />
              {touched.clubPassword && errors.clubPassword && (
                <Text style={{ fontSize: 12, color: '#FF0D10' }}>
                  {errors.clubPassword}
                </Text>
              )}
              <View style={styles.btnContainer}>
                <Button
                  title="Submit"
                  onPress={handleSubmit}
                  disabled={!isValid}
                />
              </View>
            </View>
          </TouchableWithoutFeedback>
        </KeyboardAvoidingView>
      )}
    </Formik>
  );
}

function HomeScreen({ navigation }) {
  return (
    <View style={styles.container}>
      <TouchableOpacity
        onPress={() => navigation.navigate('ClubForm')}
        style={{ backgroundColor: 'blue' }}
      >
        <Text style={{ fontSize: 20, color: '#fff' }}>Club Officer</Text>
      </TouchableOpacity>
      <TouchableOpacity
        onPress={() => navigation.navigate('AttendeeForm')}
        style={{ backgroundColor: 'red' }}
      >
        <Text style={{ fontSize: 20, color: '#fff' }}>Attendee</Text>
      </TouchableOpacity>
    </View>
  );
}

const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Home">
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="AttendeeForm" component={AttendeeForm} />
        <Stack.Screen name="ClubForm" component={ClubForm} />
        <Stack.Screen name="attendSuccess" component={attendSuccess} />
        <Stack.Screen name="clubSuccess" component={clubSuccess} />
        <Stack.Screen name="clubFail" component={clubFail} />
        <Stack.Screen name="attendFail" component={attendFail} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  logo: {
    width: 305,
    height: 159,
    marginBottom: 20,
  },
  instructions: {
    color: '#888',
    fontSize: 18,
    marginHorizontal: 15,
    marginBottom: 10,
  },
  inner: {
    padding: 24,
    flex: 1,
    justifyContent: 'space-around',
  },
  header: {
    fontSize: 36,
    marginBottom: 48,
  },
  textInput: {
    height: 40,
    borderColor: '#000000',
    borderBottomWidth: 1,
    marginBottom: 36,
  },
  btnContainer: {
    backgroundColor: 'white',
    marginTop: 12,
  },
});
