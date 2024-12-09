import flet as ft
from flet import (
    Page, AppBar, Text, TextField, TextButton, ElevatedButton,
    Column, Container, padding, colors, IconButton, icons,
    View, SnackBar, AlertDialog, Row, Card, Image, BorderRadius,
    alignment, margin, LinearGradient, animation, transform,
    ButtonStyle, RoundedRectangleBorder, Icon, MainAxisAlignment,
    CrossAxisAlignment, ScrollMode
)
from typing import Optional, List
import httpx
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000")

# Modern UI Colors
PRIMARY_COLOR = "#007AFF"  # iOS-style blue
SECONDARY_COLOR = "#5856D6"  # Deep purple
BACKGROUND_START = "#F8F9FA"  # Light gray start
BACKGROUND_END = "#FFFFFF"  # White end
CARD_COLOR = "#FFFFFF"
TEXT_PRIMARY = "#1A1A1A"
TEXT_SECONDARY = "#6C757D"

class YouTubeSummarizerApp:
    def __init__(self, page: Page):
        self.page = page
        self.page.title = "YouTube Summarizer"
        self.page.theme_mode = "light"
        self.page.padding = 20
        self.page.spacing = 10
        self.token: Optional[str] = None
        self.user_email: Optional[str] = None
        
        # Authentication Controls
        self.email_field = self._create_text_field(
            label="Email", 
            icon=icons.EMAIL, 
            keyboard_type="email"
        )
        self.password_field = self._create_text_field(
            label="Password", 
            icon=icons.LOCK, 
            password=True
        )
        
        # Register Controls
        self.reg_email_field = self._create_text_field(
            label="Email", 
            icon=icons.EMAIL, 
            keyboard_type="email"
        )
        self.reg_password_field = self._create_text_field(
            label="Password", 
            icon=icons.LOCK, 
            password=True
        )
        self.reg_confirm_password_field = self._create_text_field(
            label="Confirm Password", 
            icon=icons.LOCK, 
            password=True
        )
        
        # History Storage
        self.history_items: List[dict] = []
        
        # Main App Setup
        self.setup_routes()
    
    def _create_text_field(self, label, icon, keyboard_type=None, password=False):
        return TextField(
            label=label,
            keyboard_type=keyboard_type or "text",
            password=password,
            can_reveal_password=password,
            width=300,
            border_radius=10,
            prefix_icon=icon,
        )
    
    def setup_routes(self):
        # Initial route setup
        self.page.on_route_change = self.route_change
        self.page.go("/login")
    
    def route_change(self, route):
        self.page.views.clear()
        
        if route.route == "/login":
            self.page.views.append(self.login_view())
        elif route.route == "/register":
            self.page.views.append(self.register_view())
        elif route.route == "/home":
            self.page.views.append(self.home_view())
        elif route.route == "/history":
            self.page.views.append(self.history_view())
        
        self.page.update()
    
    def login_view(self):
        return View(
            route="/login",
            controls=[
                Container(
                    content=Column([
                        Text("YouTube Summarizer", size=24, weight="bold", color=PRIMARY_COLOR),
                        self.email_field,
                        self.password_field,
                        ElevatedButton(
                            "Login", 
                            on_click=self.login, 
                            width=300, 
                            style=ButtonStyle(bgcolor=PRIMARY_COLOR)
                        ),
                        Row([
                            Text("Don't have an account?"),
                            TextButton("Register", on_click=lambda _: self.page.go("/register"))
                        ], alignment="center")
                    ], 
                    horizontal_alignment="center", 
                    spacing=20),
                    padding=20,
                    alignment=alignment.center
                )
            ]
        )
    
    def register_view(self):
        return View(
            route="/register",
            controls=[
                Container(
                    content=Column([
                        Text("Create Account", size=24, weight="bold", color=PRIMARY_COLOR),
                        self.reg_email_field,
                        self.reg_password_field,
                        self.reg_confirm_password_field,
                        ElevatedButton(
                            "Register", 
                            on_click=self.register, 
                            width=300, 
                            style=ButtonStyle(bgcolor=PRIMARY_COLOR)
                        ),
                        Row([
                            Text("Already have an account?"),
                            TextButton("Login", on_click=lambda _: self.page.go("/login"))
                        ], alignment="center")
                    ], 
                    horizontal_alignment="center", 
                    spacing=20),
                    padding=20,
                    alignment=alignment.center
                )
            ]
        )
    
    def home_view(self):
        # Add a URL field as an instance variable
        self.url_field = TextField(
            label="YouTube Video URL",
            width=350,
            border_radius=10,
            prefix_icon=icons.LINK
        )
        
        return View(
            route="/home",
            controls=[
                AppBar(
                    title=Text("YouTube Summarizer", color=PRIMARY_COLOR),
                    actions=[
                        IconButton(icons.HISTORY, on_click=lambda _: self.page.go("/history")),
                        IconButton(icons.LOGOUT, on_click=self.logout)
                    ]
                ),
                Container(
                    content=Column([
                        self.url_field,
                        ElevatedButton(
                            "Summarize", 
                            width=350, 
                            style=ButtonStyle(bgcolor=PRIMARY_COLOR),
                            on_click=self.summarize_video
                        )
                    ], 
                    horizontal_alignment="center", 
                    spacing=20),
                    padding=20
                )
            ]
        )
    
    def history_view(self):
        return View(
            route="/history",
            controls=[
                AppBar(
                    title=Text("Summary History", color=PRIMARY_COLOR),
                    actions=[
                        IconButton(icons.HOME, on_click=lambda _: self.page.go("/home")),
                        IconButton(icons.LOGOUT, on_click=self.logout)
                    ]
                ),
                Container(
                    content=Column(
                        [self._create_history_item(item) for item in self.history_items] 
                        if self.history_items 
                        else [Text("No summary history yet", color=TEXT_SECONDARY)],
                        horizontal_alignment="center",
                        scroll=ScrollMode.AUTO
                    ),
                    padding=20
                )
            ]
        )
    
    def _create_history_item(self, item):
        return Card(
            content=Container(
                content=Column([
                    Text(f"URL: {item.get('url', 'N/A')}", color=TEXT_PRIMARY),
                    Text(f"Summary: {item.get('summary', 'N/A')}", color=TEXT_SECONDARY),
                    Text(f"Date: {item.get('date', 'N/A')}", color=TEXT_SECONDARY)
                ]),
                padding=10
            ),
            width=350,
            elevation=2
        )
    
    async def login(self, e):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{API_URL}/auth/login/", 
                    json={
                        "email": self.email_field.value,
                        "password": self.password_field.value
                    }
                )
                
                response_data = response.json()
                
                if response.status_code == 200:
                    # Store the authentication token
                    self.token = response_data.get('key')
                    self.user_email = self.email_field.value
                    
                    # Navigate to home view
                    self.page.go("/home")
                else:
                    # Extract and display error message
                    error_message = response_data.get('non_field_errors', ['Login failed'])[0]
                    self._show_snackbar(error_message)
        except httpx.RequestError as ex:
            self._show_snackbar(f"Network error: {str(ex)}")
        except Exception as ex:
            self._show_snackbar(f"Unexpected error: {str(ex)}")

    async def register(self, e):
        # Validate password match
        if self.reg_password_field.value != self.reg_confirm_password_field.value:
            self._show_snackbar("Passwords do not match")
            return
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{API_URL}/auth/registration/", 
                    json={
                        "email": self.reg_email_field.value,
                        "password1": self.reg_password_field.value,
                        "password2": self.reg_confirm_password_field.value
                    }
                )
                
                response_data = response.json()
                
                if response.status_code == 201:
                    # Registration successful
                    self._show_snackbar("Registration successful. Please login.")
                    self.page.go("/login")
                else:
                    # Extract and display error messages
                    if 'email' in response_data:
                        error_message = response_data['email'][0]
                    elif 'password1' in response_data:
                        error_message = response_data['password1'][0]
                    else:
                        error_message = "Registration failed. Please try again."
                    
                    self._show_snackbar(error_message)
        except httpx.RequestError as ex:
            self._show_snackbar(f"Network error: {str(ex)}")
        except Exception as ex:
            self._show_snackbar(f"Unexpected error: {str(ex)}")
    
    def logout(self, e):
        self.token = None
        self.user_email = None
        self.page.go("/login")
    
    def _show_snackbar(self, message):
        snackbar = SnackBar(
            content=Text(message),
            duration=3000
        )
        self.page.snack_bar = snackbar
        self.page.snack_bar.open = True
        self.page.update()

    async def summarize_video(self, e):
        # Validate URL is not empty
        if not self.url_field.value:
            self._show_snackbar("Please enter a YouTube URL")
            return
        
        # Ensure user is authenticated
        if not self.token:
            self._show_snackbar("Please login first")
            return
        
        # Create a cancellation token for timeout
        cancellation_token = asyncio.Event()
        
        try:
            # Start a timeout task
            timeout_task = asyncio.create_task(self._timeout_task(cancellation_token))
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{API_URL}/api/summaries/summarize/", 
                    json={"url": self.url_field.value},
                    headers={"Authorization": f"Token {self.token}"}
                )
                
                # Cancel the timeout if request is successful
                cancellation_token.set()
                
                # Print full response for debugging
                print("Summarize Response Status:", response.status_code)
                print("Summarize Response Headers:", dict(response.headers))
                
                response_data = response.json()
                print("Summarize Response JSON:", response_data)
                
                if response.status_code == 200:
                    # Show summary in a dialog or navigate to a summary view
                    await self.show_summary_dialog(response_data)
                else:
                    # Extract and show error message
                    error_message = response_data.get('error', 'Failed to generate summary')
                    self._show_snackbar(f"Error: {error_message}")
        
        except asyncio.TimeoutError:
            self._show_snackbar("Summarization request timed out")
        except httpx.RequestError as ex:
            self._show_snackbar(f"Network error: {str(ex)}")
        except Exception as ex:
            # Print the full exception for debugging
            import traceback
            traceback.print_exc()
            self._show_snackbar(f"Unexpected error: {str(ex)}")
        finally:
            # Ensure timeout task is cancelled
            cancellation_token.set()

    async def _timeout_task(self, cancellation_token):
        """Handle timeout for summarization request"""
        try:
            # Wait for 30 seconds or until cancelled
            await asyncio.wait_for(cancellation_token.wait(), timeout=30.0)
        except asyncio.TimeoutError:
            self._show_snackbar("Summarization request timed out")
            # Optionally, you can add additional cleanup or cancellation logic here

    async def show_summary_dialog(self, summary_data):
        # Flag to track if dialog is being closed
        is_closing = False

        def close_dialog(e):
            nonlocal is_closing
            if not is_closing:
                is_closing = True
                self.page.dialog.open = False
                self.page.update()

        # Create a dialog to show the summary
        dialog = AlertDialog(
            title=Text(summary_data.get('title', 'Summary'), weight="bold"),
            content=Column([
                Image(
                    src=summary_data.get('thumbnail_url', ''),
                    width=300,
                    height=200,
                    fit="cover"
                ),
                Text(summary_data.get('summary', 'No summary available')),
                Text(f"Duration: {summary_data.get('duration', 'N/A')} seconds")
            ]),
            actions=[
                TextButton("Close", on_click=close_dialog)
            ],
            on_dismiss=lambda _: close_dialog(None)  # Ensure dialog can be closed via other means
        )
        
        # Show the dialog
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

def main(page: Page):
    app = YouTubeSummarizerApp(page)

ft.app(target=main, view=ft.AppView.FLET_APP)