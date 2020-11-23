package servlet;

import java.io.IOException;
import java.io.PrintWriter;

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
        String firebasePassword = request.getParameter("title");

        response.setContentType("text/html");
        PrintWriter printWriter = response.getWriter();
        printWriter.print("<html>");
        printWriter.print("<body>");
        printWriter.print("<h1>We did it boys</h1>");
        printWriter.print("<p> firebasePassword :: " + firebasePassword + "</p>");

        printWriter.print("</body>");
        printWriter.print("</html>");
        printWriter.close();
    }

}
