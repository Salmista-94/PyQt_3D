
import Qt3D 2.0
import Qt3D.Renderer 2.0
import QtQuick 2.1 as QQ2

Entity {
    id: root
    objectName: "root"

    // Use the renderer configuration specified in ForwardRenderer.qml
    // and render from the mainCamera
    components: [
        FrameGraph {
            activeFrameGraph: SortedForwardRenderer {
                id: renderer
                camera: mainCamera
            }
        }
    ]

    BasicCamera {
        id: mainCamera
        position: Qt.vector3d( 0.0, 3.5, 25.0 )
        viewCenter: Qt.vector3d( 0.0, 3.5, 0.0 )
    }

    Configuration  {
        controlledCamera: mainCamera
    }

    PhongMaterial {
        id: redAdsMaterial
        ambient: Qt.rgba( 0.2, 0.0, 0.0, 1.0 )
        diffuse: Qt.rgba( 0.8, 0.0, 0.0, 1.0 )
    }

    PlaneEntity {
        id: floor

        width: 100
        height: 100
        resolution: Qt.size(20, 20)

        material: NormalDiffuseSpecularMapMaterial {
            ambient: Qt.rgba( 0.2, 0.2, 0.2, 1.0 )
            diffuse:  Qt.resolvedUrl("../exampleresources/assets/textures/pattern_09/diffuse.webp")
            specular: Qt.resolvedUrl("../exampleresources/assets/textures/pattern_09/specular.webp")
            normal:   Qt.resolvedUrl("../exampleresources/assets/textures/pattern_09/normal.webp")
            textureScale: 10.0
            shininess: 80.0
        }
    }

    TrefoilKnot {
        id: trefoilKnot
        material: redAdsMaterial
        y: 3.5
        scale: 0.5

        QQ2.ParallelAnimation {
            loops: QQ2.Animation.Infinite
            running: true

            QQ2.NumberAnimation {
                target: trefoilKnot
                property: "theta"
                from: 0; to: 360
                duration: 2000
            }

            QQ2.NumberAnimation {
                target: trefoilKnot
                property: "phi"
                from: 0; to: 360
                duration: 2000
            }
        }
    }

    Chest {
        x: -8
    }

    HousePlant {
        x: 4
        potShape: "square"
        plantType: "bamboo"
    }

    HousePlant {
        z: 4
        potShape: "triangle"
        plantType: "palm"
    }

    HousePlant {
        x: -4
        potShape: "sphere"
        plantType: "pine"
    }

    HousePlant {
        z: -4
        potShape: "cross"
        plantType: "spikes"
    }

    HousePlant {
        z: -8
        potShape: "cross"
        plantType: "palm"
        scale: 1.15
    }

    HousePlant {
        z: 8
        potShape: "cross"
        plantType: "shrub"
        scale: 1.15
    }

    Barrel {
        x: 8
    }

    Barrel {
        x: 10
        diffuseColor: "rust"
        bump: "hard_bumps"
        specular: "rust"
    }

    Barrel {
        x: 12
        diffuseColor: "blue"
        bump: "middle_bumps"
    }

    Barrel {
        x: 14
        diffuseColor: "green"
        bump: "soft_bumps"
    }

    Barrel {
        x: 16
        diffuseColor: "stainless_steel"
        bump: "no_bumps"
        specular: "stainless_steel"
        shininess: 150
    }
}
