@startuml
' C4-PlantUML
!includeurl https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml
!includeurl https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

' People
Person(dev, "App Developer", "Application developer")
Person(user, "End User")

' External systems (CI/CD and deployment)
System_Ext(train, "Train", "CI/CD train job")
System_Ext(lift, "LIFT", "Deploying images and packages")
System_Ext(webstack2, "Webstack2", "1) IAM/EIM validation\n2) CLM, LB, OIDC provision, etc.\n3) Application deployment")
System_Ext(lbv3, "LBv3", "Load Balancer")

' Execution platform (Treadmill/MKS -> cell/namespace -> pod)
Boundary(treadmill, "Treadmill/MKS") {
  Boundary(cell, "Cell / Namespace") {
    Boundary(pod, "Treadmill Instance / Pod") {
      Container(reverse, "httpd ADC", "httpd", "OIDC & ILS enforced (reverse proxy)")
      Container(app, "Application Image", "Spring Boot / Flask / .NET Core", "App container")
    }
  }
}

' Database
ContainerDb(db, "Database", "EC-supported DB", "Authenticated & authorized access")

' Relationships (image and deployment flow)
Rel(dev, train, "Curate image")
Rel(train, lift, "Promote image")
Rel(lift, pod, "Pull image", "Image")
Rel(webstack2, pod, "Deploy", "Automation")

' User traffic
Rel(user, lbv3, "HTTPS")
Rel(lbv3, reverse, "HTTPS")
Rel(reverse, app, "Proxy")
Rel(app, db, "Read/Write", "Authenticated")

' Extras (provisioning / policies)
Rel(webstack2, lift, "Package publish/approve")
Rel(webstack2, reverse, "OIDC / LB config")

SHOW_LEGEND()
@enduml
