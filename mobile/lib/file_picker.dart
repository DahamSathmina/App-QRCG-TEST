import 'package:dio/dio.dart';
import 'package:file_picker/file_picker.dart';

void uploadFile() async {
  FilePickerResult? result = await FilePicker.platform.pickFiles();
  if (result != null) {
    String path = result.files.single.path!;
    String filename = result.files.single.name;
    var formData = FormData.fromMap(
        {"file": await MultipartFile.fromFile(path, filename: filename)});
    await Dio().post("$serverIP/upload", data: formData);
  }
}
