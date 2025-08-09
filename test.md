@startuml
' C4-PlantUML
!includeurl https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml
!includeurl https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

' Personas
Person(dev, "app developer", "application developer")
Person(user, "enduser2")

' Sistemas auxiliares (CI/CD y despliegue)
System_Ext(train, "Train", "CI/CD train job")
System_Ext(lift, "LIFT", "Deploying images and packages")
System_Ext(webstack2, "webstack2", "1) IAM/EIM validation\n2) CLM, LB, OIDC provision, etc.\n3) Application deploy")
System_Ext(lbv3, "LBv3", "Load Balancer")

' Plataforma de ejecución (Treadmill/MKS -> cell/namespace -> pod)
Boundary(treadmill, "Treadmill/MKS") {
  Boundary(cell, "cell / namespace") {
    Boundary(pod, "treadmill_instance / pod") {
      Container(reverse, "httpd ADC", "httpd", "OIDC & ILS enforced (reverse proxy)")
      Container(app, "Application Image", "Spring Boot / Flask / .NET Core", "App container")
    }
  }
}

' Base de datos
ContainerDb(db, "database", "EC-supported DB", "Authenticated & authorized access")

' Relaciones (flujo de imágenes y despliegue)
Rel(dev, train, "curate image")
Rel(train, lift, "promote image")
Rel(lift, pod, "pull image", "image")
Rel(webstack2, pod, "deploy", "automation")

' Tráfico de usuarios
Rel(user, lbv3, "https")
Rel(lbv3, reverse, "https")
Rel(reverse, app, "proxy")
Rel(app, db, "read/write", "authenticated")

' Extras (provisioning / policies)
Rel(webstack2, lift, "package publish/approve")
Rel(webstack2, reverse, "OIDC / LB config")

SHOW_LEGEND()
@enduml
