import SwiftUI

struct SettingsView: View {
    @AppStorage("poolAddress") var poolAddress: String = ""
    @AppStorage("poolPort") var poolPort: String = ""
    @AppStorage("username") var username: String = ""
    @AppStorage("password") var password: String = ""
    @AppStorage("minDiff") var minDiff: String = ""

    var body: some View {
        NavigationView {
            Form {
                Section(header: Text("Pool Settings")) {
                    TextField("Pool Address", text: $poolAddress)
                    TextField("Pool Port", text: $poolPort)
                        .keyboardType(.numberPad)
                }

                Section(header: Text("User Settings")) {
                    TextField("Username", text: $username)
                    SecureField("Password", text: $password)
                }

                Section(header: Text("Mining Settings")) {
                    TextField("Minimum Difficulty", text: $minDiff)
                        .keyboardType(.decimalPad)
                }
            }
            .navigationBarTitle("Settings")
            .navigationBarItems(trailing: Button("Save") {
                saveSettings()
            })
        }
    }

    func saveSettings() {
        let configData = [
            "pool_address": poolAddress,
            "pool_port": Int(poolPort) ?? 0,
            "user_name": username,
            "password": password,
            "min_diff": Double(minDiff) ?? 0.0
        ] as [String : Any]

        if let jsonData = try? JSONSerialization.data(withJSONObject: configData, options: .prettyPrinted) {
            let jsonString = String(data: jsonData, encoding: .utf8)
            let fileManager = FileManager.default
            if let documentDirectory = fileManager.urls(for: .documentDirectory, in: .userDomainMask).first {
                let filePath = documentDirectory.appendingPathComponent("config.json")
                try? jsonString?.write(to: filePath, atomically: true, encoding: .utf8)
            }
        }
    }
}

struct SettingsView_Previews: PreviewProvider {
    static var previews: some View {
        SettingsView()
    }
}