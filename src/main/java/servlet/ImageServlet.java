package servlet;

import java.io.IOException;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet(
        name = "SpotTheLesionServlet",
        urlPatterns = {"/post"}
)
public class ImageServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String firebasePassword = request.getParameter("firebasePassword");
        String password = request.getParameter("password");

        System.out.println(System.getenv().containsKey("firebasePassword"));
    }

}
