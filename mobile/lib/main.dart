import 'package:flutter/material.dart';
import 'package:socket_io_client/socket_io_client.dart' as IO;
import 'package:dio/dio.dart';
import 'package:file_picker/file_picker.dart';

void main() => runApp(MyApp());

class MyApp extends StatefulWidget {
  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  List<String> files = [];
  late IO.Socket socket;
  final String serverIP = "http://192.168.1.100:5000"; // Desktop IP

  @override
  void initState() {
    super.initState();
    // Connect SocketIO
    socket = IO.io(
      serverIP,
      IO.OptionBuilder().setTransports(['websocket']).build(),
    );
    socket.onConnect((_) => print("Connected to Desktop NETLAB"));
    socket.on("file_added", (data) {
      setState(() => files.add(data['filename']));
    });
    socket.on("file_deleted", (data) {
      setState(() => files.remove(data['filename']));
    });
  }

  void uploadFile() async {
    FilePickerResult? result = await FilePicker.platform.pickFiles();
    if (result != null) {
      String path = result.files.single.path!;
      String filename = result.files.single.name;
      var formData = FormData.fromMap({
        "file": await MultipartFile.fromFile(path, filename: filename),
      });
      await Dio().post("$serverIP/upload", data: formData);
    }
  }

  void deleteFile(String filename) {
    socket.emit("delete_file", {"filename": filename});
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: Text("NETLAB Mobile"),
          actions: [
            IconButton(icon: Icon(Icons.upload_file), onPressed: uploadFile),
          ],
        ),
        body: ListView.builder(
          itemCount: files.length,
          itemBuilder: (_, index) {
            return ListTile(
              title: Text(files[index]),
              trailing: IconButton(
                icon: Icon(Icons.delete),
                onPressed: () => deleteFile(files[index]),
              ),
            );
          },
        ),
      ),
    );
  }
}
