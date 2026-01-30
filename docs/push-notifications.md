# Push Notifications - Implementierungsdokumentation

## Übersicht

Diese Dokumentation beschreibt die Implementierung von Push Notifications für Smartphones (iOS, Android) und Web-Browser (PWA) in der Task Management SaaS Anwendung.

## Architektur-Entscheidung

### Empfohlene Lösung: Firebase Cloud Messaging (FCM)

**Warum FCM?**
- ✅ Ein Service für Android, iOS und Web
- ✅ Kostenlos bis zu hohen Limits (unbegrenzt für kostenlose Nutzung)
- ✅ Gute Dokumentation und Community-Support
- ✅ Einfache Integration mit bestehender Architektur
- ✅ Reliable Delivery mit Retry-Mechanismus

**Alternative:** Native Services (APNs für iOS, FCM für Android, Web Push API für Browser)
- Mehr Kontrolle, aber auch mehr Komplexität

## Architektur-Übersicht

```
┌─────────────────┐
│  Task Service   │
│  User Service   │  ──┐
│  Project Service│    │
└─────────────────┘    │
                       │ Events
                       ↓
┌─────────────────────────────────┐
│   Notification Service           │
│   - Erstellt Notification        │
│   - Prüft User-Präferenzen      │
│   - Lädt Device-Tokens          │
└─────────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────┐
│   Push Notification Service      │
│   - FCM Integration              │
│   - Payload-Formatierung         │
│   - Error Handling               │
└─────────────────────────────────┘
                       │
                       ↓
            ┌──────────────────┐
            │  Firebase FCM    │
            └──────────────────┘
                       │
        ┌──────────────┼──────────────┐
        ↓              ↓              ↓
   Android App    iOS App      Web Browser
   (FCM)          (FCM)        (Service Worker)
```

## Datenbank-Schema

### Neue Tabelle: `user_devices`

```sql
CREATE TABLE user_devices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    device_token VARCHAR(255) NOT NULL,
    platform VARCHAR(20) NOT NULL CHECK (platform IN ('ios', 'android', 'web')),
    device_id VARCHAR(255),  -- Optional: Device-Identifier
    app_version VARCHAR(50),  -- Optional: App-Version
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_active_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, device_token)
);

CREATE INDEX idx_user_devices_user_id ON user_devices(user_id);
CREATE INDEX idx_user_devices_token ON user_devices(device_token);
```

### Neue Tabelle: `user_notification_preferences`

```sql
CREATE TABLE user_notification_preferences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    notification_type VARCHAR(50) NOT NULL,  -- 'task_assigned', 'task_updated', etc.
    enabled BOOLEAN DEFAULT TRUE,
    channel VARCHAR(20) DEFAULT 'push',  -- 'push', 'email', 'sms'
    quiet_hours_start TIME,  -- Optional: z.B. '22:00'
    quiet_hours_end TIME,     -- Optional: z.B. '08:00'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, notification_type, channel)
);

CREATE INDEX idx_notification_prefs_user_id ON user_notification_preferences(user_id);
```

## Backend-Implementierung

### 1. Notification Service Erweiterung

#### Neue Domain Entity: `UserDevice`

**Datei:** `backend/services/notification-service/src/domain/device.py`

```python
class UserDevice:
    """User device domain entity."""
    
    def __init__(
        self,
        user_id: str,
        device_token: str,
        platform: str,  # 'ios', 'android', 'web'
        device_id: Optional[str] = None,
        device_device_id: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self._user_id = user_id
        self._device_token = device_token
        self._platform = platform
        # ... Validierung
```

#### Neue Use Cases

**Datei:** `backend/services/notification-service/src/application/use_cases.py`

1. **RegisterDeviceUseCase**: Registriert ein neues Device für einen User
2. **UnregisterDeviceUseCase**: Entfernt ein Device
3. **SendPushNotificationUseCase**: Sendet Push-Notification über FCM

#### Neue API Routes

**Datei:** `backend/services/notification-service/src/api/routes.py`

```python
@router.post("/devices", response_model=DeviceDTO)
async def register_device(
    request: RegisterDeviceRequest,
    current_user_id: str = Depends(get_current_user_id)
):
    """Register a device for push notifications."""
    # ...

@router.delete("/devices/{device_token}")
async def unregister_device(
    device_token: str,
    current_user_id: str = Depends(get_current_user_id)
):
    """Unregister a device."""
    # ...
```

### 2. Push Notification Service

**Neuer Service:** `backend/services/push-notification-service/`

**Struktur:**
```
push-notification-service/
├── src/
│   ├── domain/
│   │   └── push_notification.py  # Domain-Model
│   ├── infrastructure/
│   │   ├── fcm_client.py         # FCM SDK Integration
│   │   └── apns_client.py        # Optional: APNs für native iOS
│   └── application/
│       └── send_push_use_case.py
└── requirements.txt
```

**FCM Client Implementierung:**

```python
# infrastructure/fcm_client.py
from firebase_admin import messaging, credentials, initialize_app

class FCMClient:
    """Firebase Cloud Messaging client."""
    
    def __init__(self):
        # Initialize Firebase Admin SDK
        cred = credentials.Certificate("path/to/service-account.json")
        initialize_app(cred)
    
    async def send_to_device(
        self,
        device_token: str,
        title: str,
        body: str,
        data: dict = None
    ) -> str:
        """Send push notification to single device."""
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            data=data or {},
            token=device_token
        )
        return messaging.send(message)
    
    async def send_to_multiple_devices(
        self,
        device_tokens: List[str],
        title: str,
        body: str,
        data: dict = None
    ) -> BatchResponse:
        """Send push notification to multiple devices."""
        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            data=data or {},
            tokens=device_tokens
        )
        return messaging.send_multicast(message)
```

### 3. Event-Integration

#### Event-Bus Setup (RabbitMQ empfohlen)

**Option 1: RabbitMQ (Production-ready)**
- Task Service publisht Events
- Notification Service subscribt Events
- Asynchrone Verarbeitung

**Option 2: HTTP Webhooks (Einfacher für MVP)**
- Task Service sendet HTTP-Request an Notification Service
- Synchron, aber einfacher zu implementieren

#### Event-Types

```python
# shared/events.py
class EventType(str, Enum):
    TASK_CREATED = "task.created"
    TASK_ASSIGNED = "task.assigned"
    TASK_UPDATED = "task.updated"
    TASK_COMPLETED = "task.completed"
    PROJECT_CREATED = "project.created"
    PROJECT_UPDATED = "project.updated"
```

#### Event-Handler im Notification Service

```python
# src/application/event_handlers.py
class TaskCreatedEventHandler:
    """Handle task created events."""
    
    async def handle(self, event: TaskCreatedEvent):
        # 1. Prüfe User-Präferenzen
        # 2. Erstelle Notification in DB
        # 3. Lade User-Devices
        # 4. Sende Push-Notifications
        pass
```

## Frontend-Implementierung

### 1. Web Push API (PWA)

**Service Worker:** `frontend/public/sw.js`

```javascript
// Service Worker für Web Push
self.addEventListener('push', function(event) {
    const data = event.data.json();
    const options = {
        body: data.body,
        icon: '/icon-192x192.png',
        badge: '/badge-72x72.png',
        data: data.data,
        actions: [
            {
                action: 'open',
                title: 'Öffnen'
            },
            {
                action: 'close',
                title: 'Schließen'
            }
        ]
    };
    
    event.waitUntil(
        self.registration.showNotification(data.title, options)
    );
});

self.addEventListener('notificationclick', function(event) {
    event.notification.close();
    
    if (event.action === 'open') {
        event.waitUntil(
            clients.openWindow(event.notification.data.url)
        );
    }
});
```

**Push-Registrierung:** `frontend/src/infrastructure/push.ts`

```typescript
export class PushNotificationService {
    async requestPermission(): Promise<NotificationPermission> {
        return await Notification.requestPermission();
    }
    
    async registerDevice(): Promise<string> {
        // 1. Service Worker registrieren
        const registration = await navigator.serviceWorker.register('/sw.js');
        
        // 2. Push-Subscription anfordern
        const subscription = await registration.pushManager.subscribe({
            userVisibleOnly: true,
            applicationServerKey: VAPID_PUBLIC_KEY
        });
        
        // 3. Subscription an Backend senden
        const response = await api.post('/api/v1/devices', {
            device_token: subscription.endpoint,
            platform: 'web',
            subscription: subscription.toJSON()
        });
        
        return subscription.endpoint;
    }
}
```

### 2. Native Mobile Apps

**Android (Kotlin):**
```kotlin
// Firebase Cloud Messaging Service
class MyFirebaseMessagingService : FirebaseMessagingService() {
    override fun onNewToken(token: String) {
        // Token an Backend senden
        api.registerDevice(token, "android")
    }
    
    override fun onMessageReceived(remoteMessage: RemoteMessage) {
        // Notification anzeigen
        sendNotification(remoteMessage.notification?.title, remoteMessage.notification?.body)
    }
}
```

**iOS (Swift):**
```swift
// AppDelegate.swift
func application(_ application: UIApplication, 
                 didRegisterForRemoteNotificationsWithDeviceToken deviceToken: Data) {
    let token = deviceToken.map { String(format: "%02.2hhx", $0) }.joined()
    // Token an Backend senden
    api.registerDevice(token: token, platform: "ios")
}

func userNotificationCenter(_ center: UNUserNotificationCenter,
                           didReceive response: UNNotificationResponse,
                           withCompletionHandler completionHandler: @escaping () -> Void) {
    // Deep Link handling
    if let taskId = response.notification.request.content.userInfo["task_id"] as? String {
        navigateToTask(taskId)
    }
}
```

## Payload-Struktur

### Standard FCM Payload

```json
{
  "notification": {
    "title": "Neue Aufgabe zugewiesen",
    "body": "Du hast eine neue Aufgabe 'Design Mockups erstellen' erhalten",
    "sound": "default",
    "badge": 1
  },
  "data": {
    "type": "task_assigned",
    "task_id": "uuid-here",
    "project_id": "uuid-here",
    "action": "open_task",
    "url": "/tasks/uuid-here"
  },
  "android": {
    "priority": "high",
    "notification": {
      "channel_id": "task_notifications",
      "sound": "default"
    }
  },
  "apns": {
    "headers": {
      "apns-priority": "10"
    },
    "payload": {
      "aps": {
        "sound": "default",
        "badge": 1
      }
    }
  }
}
```

## User-Präferenzen

### API Endpoints

```python
# GET /api/v1/notification-preferences
# POST /api/v1/notification-preferences
# PUT /api/v1/notification-preferences/{id}
```

### Beispiel-Präferenzen

```json
{
  "user_id": "uuid",
  "preferences": [
    {
      "notification_type": "task_assigned",
      "enabled": true,
      "channel": "push"
    },
    {
      "notification_type": "task_updated",
      "enabled": false,
      "channel": "push"
    },
    {
      "notification_type": "project_created",
      "enabled": true,
      "channel": "push",
      "quiet_hours_start": "22:00",
      "quiet_hours_end": "08:00"
    }
  ]
}
```

## Error Handling

### Token-Invalidierung

```python
# Wenn FCM "InvalidRegistration" oder "NotRegistered" zurückgibt
async def handle_invalid_token(device_token: str):
    """Remove invalid device token from database."""
    db.query(UserDeviceModel).filter(
        UserDeviceModel.device_token == device_token
    ).delete()
    db.commit()
```

### Retry-Logik

```python
async def send_with_retry(device_token: str, payload: dict, max_retries: int = 3):
    """Send push notification with exponential backoff retry."""
    for attempt in range(max_retries):
        try:
            return await fcm_client.send_to_device(device_token, payload)
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                await asyncio.sleep(wait_time)
            else:
                # Log to dead letter queue
                await log_failed_notification(device_token, payload, str(e))
```

## Rate Limiting

### Implementierung

```python
from collections import defaultdict
from datetime import datetime, timedelta

class RateLimiter:
    """Rate limiter for push notifications."""
    
    def __init__(self, max_notifications: int = 10, window_minutes: int = 60):
        self.max_notifications = max_notifications
        self.window = timedelta(minutes=window_minutes)
        self.user_notifications = defaultdict(list)
    
    def can_send(self, user_id: str) -> bool:
        """Check if user can receive notification."""
        now = datetime.utcnow()
        cutoff = now - self.window
        
        # Remove old notifications
        self.user_notifications[user_id] = [
            ts for ts in self.user_notifications[user_id] if ts > cutoff
        ]
        
        return len(self.user_notifications[user_id]) < self.max_notifications
    
    def record_sent(self, user_id: str):
        """Record that notification was sent."""
        self.user_notifications[user_id].append(datetime.utcnow())
```

## Monitoring & Analytics

### Metriken tracken

```python
# Metriken pro Notification
- sent_at: Timestamp
- delivered_at: Timestamp (von FCM bestätigt)
- opened_at: Timestamp (User öffnet Notification)
- clicked_at: Timestamp (User klickt auf Action)
- error: Error-Message falls fehlgeschlagen
```

### Dashboard-Metriken

- **Delivery Rate**: Erfolgreich gesendet / Gesamt
- **Open Rate**: Geöffnet / Gesendet
- **Click-Through Rate**: Geklickt / Gesendet
- **Error Rate**: Fehler / Gesamt
- **Platform Distribution**: iOS / Android / Web

## Sicherheit

### Best Practices

1. **Token-Verschlüsselung**: Device-Tokens verschlüsselt in DB speichern
2. **HTTPS Only**: Alle API-Calls über HTTPS
3. **JWT Authentication**: Device-Registrierung nur mit gültigem JWT
4. **Rate Limiting**: Pro User und pro Device
5. **Input Validation**: Alle Payloads validieren
6. **VAPID Keys**: Für Web Push sicher speichern

## Deployment-Checkliste

### Firebase Setup

1. ✅ Firebase-Projekt erstellen
2. ✅ Service Account Key generieren
3. ✅ FCM API aktivieren
4. ✅ VAPID Keys für Web Push generieren
5. ✅ Service Account Key sicher speichern (Environment Variable)

### Backend

1. ✅ `firebase-admin` SDK installieren
2. ✅ FCM Client implementieren
3. ✅ Device-Registrierung API
4. ✅ Push-Send-Logik
5. ✅ Error Handling & Retry
6. ✅ Rate Limiting
7. ✅ User-Präferenzen API

### Frontend

1. ✅ Service Worker registrieren
2. ✅ Push-Permission anfordern
3. ✅ Device-Token an Backend senden
4. ✅ Notification-Click-Handling
5. ✅ Deep Linking implementieren

### Testing

1. ✅ Unit Tests für FCM Client
2. ✅ Integration Tests für Device-Registrierung
3. ✅ E2E Tests für Push-Flow
4. ✅ Error-Szenarien testen

## Beispiel-Flow: Task erstellt

```
1. User erstellt Task über Frontend
   ↓
2. Frontend sendet POST /api/v1/tasks
   ↓
3. Task Service erstellt Task in DB
   ↓
4. Task Service publisht Event: "task.created"
   ↓
5. Notification Service empfängt Event
   ↓
6. Notification Service prüft:
   - User-Präferenzen (task_created erlaubt?)
   - Rate Limits (nicht zu viele Notifications?)
   - Quiet Hours (aktuelle Zeit erlaubt?)
   ↓
7. Notification Service erstellt Notification in DB
   ↓
8. Notification Service lädt alle User-Devices
   ↓
9. Push Service formatiert Payload:
   {
     "title": "Neue Aufgabe erstellt",
     "body": "Task 'Design Mockups' wurde erstellt",
     "data": {
       "type": "task_created",
       "task_id": "uuid",
       "action": "open_task"
     }
   }
   ↓
10. Push Service sendet an FCM:
    - Android Device Token → FCM
    - iOS Device Token → FCM
    - Web Subscription → FCM
   ↓
11. FCM liefert an Devices:
    - Android: System Notification
    - iOS: System Notification
    - Web: Browser Notification (Service Worker)
   ↓
12. User sieht Notification
   ↓
13. User klickt → Deep Link öffnet App/Web → Task-Detail
```

## Nächste Schritte

1. **Phase 1 (MVP)**: Web Push Notifications
   - Service Worker implementieren
   - Device-Registrierung
   - Einfache Push-Benachrichtigungen

2. **Phase 2**: Event-Integration
   - RabbitMQ/Event-Bus Setup
   - Event-Handler im Notification Service
   - Automatische Benachrichtigungen

3. **Phase 3**: User-Präferenzen
   - Preferences API
   - UI für Einstellungen
   - Quiet Hours

4. **Phase 4**: Native Apps
   - Android App mit FCM
   - iOS App mit FCM
   - Deep Linking

5. **Phase 5**: Advanced Features
   - Batching (mehrere Events → eine Notification)
   - Rich Notifications (Bilder, Actions)
   - Analytics Dashboard

## Ressourcen

- [Firebase Cloud Messaging Dokumentation](https://firebase.google.com/docs/cloud-messaging)
- [Web Push API](https://developer.mozilla.org/en-US/docs/Web/API/Push_API)
- [FCM Python Admin SDK](https://firebase.google.com/docs/reference/admin/python)
- [PWA Push Notifications Guide](https://web.dev/push-notifications-overview/)
