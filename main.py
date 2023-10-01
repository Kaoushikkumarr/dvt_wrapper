from data_decoupling_automation.app import create_app

if __name__ == "__main__":
    create_app().run(host="localhost", port=8080, debug=False)
