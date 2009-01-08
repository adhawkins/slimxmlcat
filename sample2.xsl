<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:strip-space elements="*"/>
	
	<xsl:template match="/">
	  <html>
	  <body>
	    <h2>My CD Collection</h2>
	    <table border="1">
				<tr bgcolor="#9acd32">
					<th align="left">Title</th>
					<th align="left">Artist</th>
					<th align="left">Cover art</th>
				</tr>
				<xsl:apply-templates select="catalogue"/>
	    </table>
	  </body>
	  </html>
	</xsl:template>
	
	<xsl:template match="catalogue/album">
		<tr>
			<td><xsl:value-of select="name"/></td>
			<td><xsl:value-of select="artist"/></td>
			<td>
				<img width="100">
				<xsl:attribute name="src"><xsl:value-of select="artwork"/></xsl:attribute>
				</img>
			</td>
		</tr>
		<xsl:apply-templates select="tracks"/>
	</xsl:template>

	<xsl:template match="tracks">
		<tr>
			<td colspan="3">
				<table width="100%" border="1">
					<xsl:apply-templates/>
				</table>
			</td>
		</tr>		
	</xsl:template>
	
	<xsl:template match="track">
		<tr>
			<td><xsl:value-of select="@number"/></td>
			<td><xsl:value-of select="title"/></td>
			<td><xsl:value-of select="duration"/></td>
			<td><xsl:value-of select="artist"/></td>
		</tr>	
	</xsl:template>
</xsl:stylesheet>
