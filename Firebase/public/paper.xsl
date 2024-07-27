<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" indent="yes"/>

    <xsl:template match="/">
        <html>
        <head>
            <!-- <title>Paper Details</title> -->
            <h3><xsl:value-of select="paper/title"/></h3>
        </head>
        <body>
            <!-- <h2>Paper Details</h2> -->
            
            <p><strong>Year:</strong> <xsl:value-of select="paper/year"/></p>
            <p><strong>Authors:</strong>
                <ul>
                    <xsl:for-each select="paper/authors/author">
                        <li><xsl:value-of select="."/></li>
                    </xsl:for-each>
                </ul>
            </p>
            <p><strong>Document Type:</strong> <xsl:value-of select="paper/doc_type"/></p>
            <!-- <p><strong>References:</strong>
                <ul>
                    <xsl:for-each select="paper/references/reference">
                        <li><xsl:value-of select="."/></li>
                    </xsl:for-each>
                </ul>
            </p> -->
            <p><strong>Venue:</strong> <xsl:value-of select="paper/venue"/></p>
            <p><strong>DOI:</strong> <xsl:value-of select="paper/doi"/></p>
            <p><strong>Publisher:</strong> <xsl:value-of select="paper/publisher"/></p>
            <p><strong>Abstract:</strong> <xsl:value-of select="paper/abstract"/></p>
        </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
