package com.gb.bci.ant.taskdefs;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;
import java.util.regex.Pattern;
import java.util.regex.Matcher;
import java.util.regex.PatternSyntaxException;
import org.apache.tools.ant.BuildException;
import org.apache.tools.ant.Project;
import org.apache.tools.ant.Task;

/**
 * Converts text log files from compilers e.g.
 * To the format that CruiseControl expects when
 * merging logfiles.
 *
 * Based on work by Tony Cook available on the CruiseControl wiki
 * at http://confluence.public.thoughtworks.org/display/CC/UsingCruiseControlWithCplusPlus
 *
 * Created: Wed Mar 14 10:21:05 2007
 *
 * @author <a href="mailto:PoutanenIlkka@JohnDeere.com">Ilkka Poutanen</a>
 * @version 1.0
 */
public class TextToCCXml extends Task {

    private File m_srcfile;

    private File m_destfile;

    private boolean m_isError;

    private String m_target;

    private String m_task;

    public void setSrcfile(File srcfile)
    {
	m_srcfile = srcfile;
    }

    public void setDestfile(File destfile)
    {
	m_destfile = destfile;
    }

    public void setIsError(boolean error)
    {
	m_isError = error;
    }

    public void setTarget(String target)
    {
	m_target = target;
    }

    public void setTask(String task)
    {
	m_task = task;
    }

    public void execute() throws BuildException
    {
	validate();

	BufferedReader reader = null;
	FileOutputStream output = null;
	PrintWriter writer = null;
	try {
	    reader = new BufferedReader(new FileReader(m_srcfile));
	    output = new FileOutputStream(m_destfile);
	    writer = new PrintWriter(new OutputStreamWriter(output, "UTF-8"));

	    // add header and toplevel tags
	    writer.println("<?xml version=\"1.0\" encoding=\"UTF-8\"?>");
	    writer.print("<build");
	    if (m_isError) {
		writer.print(" error=\"Target " + m_target + " failed\"");
	    }
	    writer.println(" time=\"0 hours 00 minuts 00 seconds\">");
	    writer.println("<target name=\"" + m_target + "\" time=\"ignored\">");
	    writer.println("<task location=\"ignored\" name=\"" + m_task + "\" time=\"ignored\">");

	    // prepare regex patterns for warning/error matching
	    Pattern p_w = null;
	    Pattern p_e = null;
	    try {
		p_w = Pattern.compile(".*\\bwarning\\b.*", Pattern.CASE_INSENSITIVE);
		p_e = Pattern.compile(".*\\berror\\b.*", Pattern.CASE_INSENSITIVE);
	    } catch (PatternSyntaxException pse) {
		throw new BuildException(pse.toString(), pse);
	    }

	    // okay, output filtered messages from sourcefile
	    String line = reader.readLine();
	    while(null != line) {
		// print the tag
		writer.print(" <message priority=\"");
		// check if it's a warning or error
		Matcher m_w = p_w.matcher(line);
		Matcher m_e = p_e.matcher(line);
		if (m_w.matches()) {
		    writer.print("warn");
		} else if (m_e.matches()) {
		    writer.print("error");
		} else {
		    writer.print("info");
		}
		writer.print("\">");

		// filter nulls
		line = line.replace('\0', ' ');

		// print the rest
		writer.print("<![CDATA[");
		writer.print(line);
		writer.println("]]></message>");

		// next line
		line = reader.readLine();
	    }

	    // close the XML
	    writer.println("</task>");
	    writer.println("</target>");
	    writer.println("</build>");
	    writer.flush();
	    writer.close();
	} catch(UnsupportedEncodingException uee) {
	    log(uee.toString(), Project.MSG_ERR);
	} catch(IOException ioe) {
	    throw new BuildException(ioe.toString(), ioe);
	} finally {
	    if (null != reader) {
		try { reader.close(); } catch(IOException e) {}
	    }
	    if (null != output) {
		try { output.close(); } catch(IOException e) {}
	    }
	}
    }

    private void validate() throws BuildException
    {
	if (null == m_srcfile) {
	    throw new BuildException("SrcFile must be set.");
	}

	if (null == m_destfile) {
	    throw new BuildException("DestFile must be set.");
	}

	if (null == m_target) {
	    throw new BuildException("Target must be set");
	}

	if (null == m_task) {
	    throw new BuildException("Task must be set");
	}
    }
}