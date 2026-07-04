import "./index.css";
import { Composition } from "remotion";
import { HelloWorld, myCompSchema } from "./HelloWorld";
import { Logo, myCompSchema2 } from "./HelloWorld/Logo";
import { FadeInOut } from "./Stage1_Interpolation/FadeInOut";
import { Transformations } from "./Stage1_Interpolation/Transformations";
import { PulsingServer } from "./Stage1_Interpolation/PulsingServer";
import { BounceIn } from "./Stage2_Springs/BounceIn";
import { StaggeredList } from "./Stage2_Springs/StaggeredList";
import { DatabaseCluster } from "./Stage2_Springs/DatabaseCluster";
import { RequestRouter } from "./Stage3_SVG/RequestRouter";
import { SharinganIntro, sharinganSchema } from "./Stage3_SVG/SharinganIntro";
import { TechExplainer } from "./Stage4_Audio/TechExplainer";

// Each <Composition> is an entry in the sidebar!

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="stage3-request-router"
        component={RequestRouter}
        durationInFrames={180}
        fps={30}
        width={1920}
        height={1080}
      />

      <Composition
        id="stage3-sharingan-intro"
        component={SharinganIntro}
        durationInFrames={180}
        fps={30}
        width={1920}
        height={1080}
        schema={sharinganSchema}
        defaultProps={{
          eyeballGlowColor: "rgba(182, 0, 240, 0.45)",
          irisScaleFactor: 0.45,
          pupilRadius: 30,
          rotations: 6,
          veinsOpacity: 0.15,
          enableJitter: true,
        }}
      />

      <Composition
        id="stage4-tech-explainer"
        component={TechExplainer}
        durationInFrames={300}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="stage2-bounce-in"
        component={BounceIn}
        durationInFrames={90}
        fps={30}
        width={1920}
        height={1080}
      />

      <Composition
        id="stage2-staggered-list"
        component={StaggeredList}
        durationInFrames={120}
        fps={30}
        width={1920}
        height={1080}
      />

      <Composition
        id="stage2-database-cluster"
        component={DatabaseCluster}
        durationInFrames={150}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="stage1-fade-in-out"
        component={FadeInOut}
        durationInFrames={90}
        fps={30}
        width={1920}
        height={1080}
      />

      <Composition
        id="stage1-transformations"
        component={Transformations}
        durationInFrames={90}
        fps={30}
        width={1920}
        height={1080}
      />

      <Composition
        id="stage1-pulsing-server"
        component={PulsingServer}
        durationInFrames={150}
        fps={30}
        width={1920}
        height={1080}
      />

      <Composition
        // You can take the "id" to render a video:
        // npx remotion render HelloWorld
        id="HelloWorld"
        component={HelloWorld}
        durationInFrames={150}
        fps={30}
        width={1920}
        height={1080}
        // You can override these props for each render:
        // https://www.remotion.dev/docs/parametrized-rendering
        schema={myCompSchema}
        defaultProps={{
          titleText: "Welcome to my rdx dev creator lab",
          titleColor: "#000000",
          logoColor1: "#91EAE4",
          logoColor2: "#86A8E7",
        }}
      />

      {/* Mount any React component to make it show up in the sidebar and work on it individually! */}
      <Composition
        id="OnlyLogo"
        component={Logo}
        durationInFrames={150}
        fps={30}
        width={1920}
        height={1080}
        schema={myCompSchema2}
        defaultProps={{
          logoColor1: "#91dAE2" as const,
          logoColor2: "#86A8E7" as const,
        }}
      />
    </>
  );
};
