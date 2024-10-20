import Header from "./components/Header";
import Menu from "./components/Menu";
import Footer from "./components/Footer";
import Camera from "./components/Camera";

const App = () => {
  return (
    <div style={{ height: "100vh" }}>
      <Header></Header>

      <div className="flex-container">
        <div className="flex-item">
          <Menu />
        </div>
        <div className="flex-item camera">
          <Camera />
        </div>
      </div>
      <Footer></Footer>
    </div>
  );
};

export default App;
