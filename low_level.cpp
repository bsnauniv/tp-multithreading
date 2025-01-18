#include <Eigen/Dense>
#include <chrono>
#include <cpr/cpr.h>
#include <iostream>
#include <nlohmann/json.hpp>

using json = nlohmann::json;
using namespace Eigen;
using namespace std;
using namespace chrono;

constexpr char SERVER_URL[] = "http://127.0.0.1:8000/";
constexpr char CONTENT_TYPE[] = "application/json";

class Task {
public:
  int identifier;
  int size;
  MatrixXf a;
  VectorXf b;
  VectorXf x;
  float time;

  Task(int id, int s, MatrixXf &a1, VectorXf &b1, VectorXf &x1, float t)
      : identifier(id), size(s), a(a1), b(b1), x(x1), time(t) {}

  json to_json() const {
    json j;
    j["identifier"] = identifier;
    j["size"] = size;

    // Conversion des matrices et vecteurs en tableaux pour JSON
    j["a"] = json::array();
    for (int i = 0; i < size; ++i) {
      std::vector<float> row(a.row(i).data(), a.row(i).data() + size);
      j["a"].push_back(row);
    }
    j["b"] = std::vector<float>(b.data(), b.data() + size);
    j["x"] = std::vector<float>(x.data(), x.data() + size);
    j["time"] = time;

    return j;
  }

  static Task from_json(const json &j) {
    int id = j["identifier"];
    int size = j["size"];

    MatrixXf a(size, size);
    for (int i = 0; i < size; ++i)
      for (int j_idx = 0; j_idx < size; ++j_idx)
        a(i, j_idx) = j["a"][i][j_idx];

    VectorXf b(size), x(size);
    for (int i = 0; i < size; ++i) {
      b(i) = j["b"][i];
      x(i) = j["x"][i];
    }

    float time = j["time"];

    return Task(id, size, a, b, x, time);
  }

  void work() {
    auto start = std::chrono::high_resolution_clock::now();
    x = a.colPivHouseholderQr().solve(b); // Résolution avec Eigen
    auto end = std::chrono::high_resolution_clock::now();

    time = std::chrono::duration<float>(end - start).count();
  }
};

int main() {
  // Requête GET pour récupérer les données de tâche
  cpr::Response r = cpr::Get(cpr::Url{"http://127.0.0.1:8000"});
  if (r.status_code != 200) {
    cerr << "Erreur HTTP GET : " << r.status_code << " - " << r.text << endl;
    return 1;
  }

  // Désérialisation des données JSON en objet Task
  json j_data = json::parse(r.text);
  Task t = Task::from_json(j_data);

  cout << "Task received - ID : " << t.identifier << ", Size : " << t.size
       << endl;

  // Résolution du système linéaire
  t.work();
  cout << "Duration : " << t.time << " s" << endl;

  // Sérialisation en JSON après calcul
  json j_result = t.to_json();

  // Envoi des résultats via une requête POST
  cpr::Response post_response =
      cpr::Post(cpr::Url{"http://localhost:8000"},
                cpr::Header{{"Content-Type", "application/json"}},
                cpr::Body{j_result.dump()});

  // Vérification de la réponse POST
  if (post_response.status_code == 200) {
    cout << "Result sent !" << endl;
  } else {
    cerr << "Erreur HTTP POST : " << post_response.status_code << " - "
         << post_response.text << endl;
  }

  return 0;
}
