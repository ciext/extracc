<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:output encoding="utf-8" indent="yes"/>

	<xsl:template match="TestRun">
		<testsuite name="{normalize-space(substring-before(//Name, '::'))}"
			tests="{normalize-space(Statistics/Tests)}"
			failures="{normalize-space(Statistics/Failures)}"
			errors="{normalize-space(Statistics/Errors)}"
			time="-1">
			<xsl:apply-templates/>
		</testsuite>
	</xsl:template>

	<xsl:template match="FailedTests">
		<xsl:apply-templates/>
	</xsl:template>

	<xsl:template match="SuccessfulTests">
		<xsl:apply-templates/>
	</xsl:template>

	<xsl:template match="Test">
		<testcase name="{normalize-space(substring-after(Name, '::'))}" time="-1" />
	</xsl:template>

	<xsl:template match="FailedTest">
		<testcase name="{normalize-space(substring-after(Name, '::'))}" time="-1">
			<failure>
				<xsl:value-of select="concat(
					normalize-space(FailureType),
					': ',
					normalize-space(Location/File),
					' at line ',
					normalize-space(Location/Line))" />
				<br/>
				<xsl:value-of select="normalize-space(Message)" />
			</failure>
		</testcase>
	</xsl:template>

	<xsl:template match="Statistics">
	</xsl:template>

</xsl:stylesheet>